import argparse
import json
import os
import time
from typing import List, Dict

import anthropic  # pip install anthropic

from world import build_catalogue, code_summary
from oracle import Oracle


def load_instructions(path="instructions.md"):
    with open(path) as f:
        return f.read()


def tool_specs(alphabet: str) -> List[dict]:
    # Deliberately minimal. No mention of codons, residues, length, or folding.
    return [
        {
            "name": "query",
            "description": (
                "Submit one sequence to the organism and receive a number "
                "(the outcome). Higher is better. The sequence may use only "
                f"these characters: {', '.join(alphabet)}. "
                "Only ONE query is performed per turn — if you issue more "
                "than one query in a single message, only the first will be "
                "executed and the rest will be refused. After each query you "
                "may write to your notebook and then issue the next query."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "sequence": {"type": "string",
                                 "description": f"A string over {{{', '.join(alphabet)}}}."},
                    "rationale": {"type": "string",
                                  "description": "What hypothesis this experiment tests."},
                },
                "required": ["sequence", "rationale"],
            },
        },
        {
            "name": "write_notebook",
            "description": (
                "Append an entry to your lab notebook. APPEND-ONLY: never "
                "rewrite prior entries. Record your current theory, what your "
                "last experiments showed, and what you will test next and why."
            ),
            "input_schema": {
                "type": "object",
                "properties": {"entry": {"type": "string"}},
                "required": ["entry"],
            },
        },
    ]


def _mark_caching(messages):
    """Set ephemeral cache_control on the trailing block of the LAST user
    message; strip it from any earlier user messages.

    Why this pattern: Anthropic prompt caching uses a marker on the last block
    that should be cached. Everything before & including that marker becomes
    the cache prefix for the *next* request. Each turn we move the marker
    forward, so each call reads the full prior conversation from cache and
    only processes the newest delta. The API caps at 4 breakpoints, so we
    keep exactly one rolling user-message breakpoint (plus the system-prompt
    breakpoint set elsewhere)."""
    last_user_idx = None
    for i, m in enumerate(messages):
        if m["role"] != "user":
            continue
        # Normalize bare-string content into list form so we can attach a
        # cache_control field to the last block.
        if isinstance(m["content"], str):
            m["content"] = [{"type": "text", "text": m["content"]}]
        # Strip cache_control from earlier user messages.
        for blk in m["content"]:
            if isinstance(blk, dict) and "cache_control" in blk:
                del blk["cache_control"]
        last_user_idx = i
    if last_user_idx is not None:
        last_blocks = messages[last_user_idx]["content"]
        if isinstance(last_blocks, list) and last_blocks and isinstance(last_blocks[-1], dict):
            last_blocks[-1]["cache_control"] = {"type": "ephemeral"}


def call_model(client, model, system, messages, tools, max_tokens=4096):
    # System prompt is cacheable too — wrap as a list block so we can mark it.
    if isinstance(system, str):
        system = [{"type": "text", "text": system,
                   "cache_control": {"type": "ephemeral"}}]
    _mark_caching(messages)
    return client.messages.create(
        model=model, max_tokens=max_tokens, system=system,
        tools=tools, messages=messages,
    )


def run(
    world_name: str,
    n_residues: int = 16,
    budget: int = 300,
    model: str = "claude-opus-4-7",
    out_dir: str = "runs",
    table_path: str = "table_16.bin",
    contacts_path: str = "contacts_16.bin",
    instructions_path: str = "instructions.md",
    seed_tag: str = "",
):
    cat = build_catalogue()
    if world_name not in cat:
        raise SystemExit(f"unknown world {world_name}; choices: {list(cat)}")
    world = cat[world_name]

    label = world_name + (f"_{seed_tag}" if seed_tag else "")
    run_dir = os.path.join(out_dir, label)
    os.makedirs(run_dir, exist_ok=True)
    notebook_path = os.path.join(run_dir, "notebook.md")
    transcript_path = os.path.join(run_dir, "transcript.jsonl")
    query_log = os.path.join(run_dir, "queries.jsonl")
    state_path = os.path.join(run_dir, "state.json")

    # Auto-resume if a prior checkpoint exists; otherwise fresh start.
    resuming = os.path.isfile(state_path)
    if not resuming:
        open(notebook_path, "w").close()
        open(transcript_path, "w").close()
        # Ground truth for the human's post-hoc read (NEVER shown to the agent).
        with open(os.path.join(run_dir, "GROUND_TRUTH.json"), "w") as f:
            json.dump(code_summary(world), f, indent=2)

    oracle = Oracle(world, n_residues=n_residues, table_path=table_path,
                    contacts_path=contacts_path, log_path=query_log,
                    resume=resuming)

    # Load instructions and substitute per-world placeholders. Each world
    # exposes its own sequence-length (codon_length * n_residues) so the
    # agent isn't forced to discover the magic length cold.
    system = load_instructions(instructions_path)
    n_chars = world.codon_length * n_residues
    system = system.replace("{n_chars}", str(n_chars))
    # Vertex (sabeti-ai, global endpoint) — same auth path as MPRAgent / Fable
    # runs in this project. Pull project/region from env so they can be
    # overridden per-run without code edits.
    client = anthropic.AnthropicVertex(
        project_id=os.environ.get("ANTHROPIC_VERTEX_PROJECT_ID", "sabeti-ai"),
        region=os.environ.get("CLOUD_ML_REGION", "global"),
    )
    tools = tool_specs(world.alphabet)

    # The intro reveals ONLY the alphabet and the budget. Nothing structural.
    intro = (
        f"You may use the characters {{{', '.join(world.alphabet)}}}. "
        f"You have {budget} experiments. Begin by writing an initial notebook "
        f"entry with your starting assumptions and first experiment, then start."
    )

    if resuming:
        # Restore prior conversation + counters. Serialized form is plain dicts
        # (Anthropic API accepts dict content blocks for replay).
        with open(state_path) as f:
            state = json.load(f)
        messages: List[Dict] = state["messages"]
        oracle.n_queries = state["n_queries"]
        oracle.best_fitness = state["best_fitness"]
        oracle.best_dna = state["best_dna"]
        print(f"[resume] picking up at query {oracle.n_queries}/{budget} "
              f"(best fitness so far: {oracle.best_fitness})", flush=True)
    else:
        messages: List[Dict] = [{"role": "user", "content": intro}]

    def log_transcript(obj):
        with open(transcript_path, "a") as f:
            f.write(json.dumps(obj) + "\n")

    def _serialize_content(content):
        # content can be a string, list of dicts (user/tool_result), or list of
        # SDK content blocks (assistant). Normalize to plain JSON-able dicts.
        if isinstance(content, str):
            return content
        out = []
        for c in content:
            if isinstance(c, dict):
                out.append(c)
            else:
                out.append(c.model_dump())
        return out

    def save_state():
        # Atomic write so an interrupt mid-write can't leave a half-file.
        snap = {
            "messages": [{"role": m["role"],
                          "content": _serialize_content(m["content"])}
                         for m in messages],
            "n_queries": oracle.n_queries,
            "best_fitness": oracle.best_fitness,
            "best_dna": oracle.best_dna,
        }
        tmp = state_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(snap, f)
        os.replace(tmp, state_path)

    def append_notebook(entry, tag=None):
        stamp = time.strftime("%Y-%m-%d %H:%M")
        header = f"FINAL" if tag == "final" else f"query {oracle.n_queries}"
        with open(notebook_path, "a") as f:
            f.write(f"\n## {stamp} — {header}\n\n{entry}\n")

    while oracle.n_queries < budget:
        resp = call_model(client, model, system, messages, tools)
        u = resp.usage
        # Track cache hit rate so it's visible in the run log.
        cr = getattr(u, "cache_read_input_tokens", 0) or 0
        cw = getattr(u, "cache_creation_input_tokens", 0) or 0
        log_transcript({"role": "assistant",
                        "content": [b.model_dump() for b in resp.content],
                        "usage": {"input": u.input_tokens, "output": u.output_tokens,
                                  "cache_read": cr, "cache_write": cw}})
        messages.append({"role": "assistant", "content": resp.content})

        # Process ANY tool_use blocks in the response, regardless of
        # stop_reason. Even when stop_reason is "max_tokens" or "refusal", the
        # response may still contain a complete tool_use block that the API
        # requires us to answer with a matching tool_result; skipping that here
        # leaves an orphaned tool_use that 400s on the next call.
        has_tool_use = any(b.type == "tool_use" for b in resp.content)
        if not has_tool_use:
            remaining = budget - oracle.n_queries
            messages.append({"role": "user", "content":
                             f"You did not issue any tool call. You have "
                             f"{remaining} experiments remaining. You must use "
                             f"all of them — there is no early stopping. Even "
                             f"after you have a working theory, use remaining "
                             f"experiments to test edge cases, probe your "
                             f"predictions, and refine your understanding. "
                             f"Issue your next query now."})
            save_state()
            continue

        tool_results = []
        query_done_this_turn = False  # enforce one-probe-per-turn
        for block in resp.content:
            if block.type != "tool_use":
                continue
            if block.name == "query":
                if query_done_this_turn:
                    # Refuse extra queries in the same turn; the API still
                    # requires a tool_result for every tool_use block.
                    tool_results.append({"type": "tool_result",
                                         "tool_use_id": block.id,
                                         "content": json.dumps({
                                             "ok": False,
                                             "refused": True,
                                             "reason": ("Only one query per turn is permitted. "
                                                        "This experiment was NOT performed and "
                                                        "no budget was consumed for it. "
                                                        "Re-issue it next turn if you still want to."),
                                             "experiments_used": oracle.n_queries,
                                             "experiments_left": budget - oracle.n_queries,
                                         })})
                    continue
                seq = block.input.get("sequence", "")
                result = oracle.query(seq)
                payload = {"ok": result["ok"], "fitness": result["fitness"],
                           "experiments_used": oracle.n_queries,
                           "experiments_left": budget - oracle.n_queries}
                tool_results.append({"type": "tool_result",
                                     "tool_use_id": block.id,
                                     "content": json.dumps(payload)})
                query_done_this_turn = True
            elif block.name == "write_notebook":
                append_notebook(block.input.get("entry", ""))
                tool_results.append({"type": "tool_result",
                                     "tool_use_id": block.id,
                                     "content": "notebook entry appended."})
            else:
                # Unknown / hallucinated tool name — still must answer it.
                tool_results.append({"type": "tool_result",
                                     "tool_use_id": block.id,
                                     "content": json.dumps({
                                         "ok": False,
                                         "error": f"unknown tool {block.name!r}; "
                                                  f"available tools are: query, write_notebook",
                                     }),
                                     "is_error": True})
        # If the turn used tools (e.g. write_notebook) but did NOT run a query,
        # push back the same way as a no-tool turn: budget must be exhausted.
        if not query_done_this_turn:
            remaining = budget - oracle.n_queries
            tool_results.append({"type": "text",
                "text": (f"You did not run an experiment this turn. You have "
                         f"{remaining} experiments remaining. You must use all "
                         f"of them — there is no early stopping. Even after you "
                         f"have a working theory, use remaining experiments to "
                         f"test edge cases, probe your predictions, and refine "
                         f"your understanding. Issue your next query now.")})
        messages.append({"role": "user", "content": tool_results})
        save_state()

        if oracle.n_queries >= budget:
            messages.append({"role": "user", "content":
                             "Your experiment budget is exhausted. Write your "
                             "final notebook entry: your best account of how "
                             "this organism works, your best sequence, and what "
                             "you would test next."})
            final = call_model(client, model, system, messages, tools)
            log_transcript({"role": "assistant_final",
                            "content": [b.model_dump() for b in final.content]})
            for block in final.content:
                if block.type == "tool_use" and block.name == "write_notebook":
                    append_notebook(block.input.get("entry", ""), tag="final")
            break

    summary = {
        "world": world_name, "n_residues": n_residues, "budget": budget,
        "queries_used": oracle.n_queries,
        "best_fitness": oracle.best_fitness, "best_sequence": oracle.best_dna,
    }
    if oracle.table and oracle.table.loaded:
        _, best_fit = oracle.table.true_optimum()
        summary["true_optimum_fitness"] = best_fit
        summary["fraction_of_optimum"] = (
            round(oracle.best_fitness / best_fit, 4)
            if (oracle.best_fitness and best_fit) else None)
    with open(os.path.join(run_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))
    print(f"\nRun complete. Read {notebook_path} against "
          f"{os.path.join(run_dir, 'GROUND_TRUTH.json')} for the qualitative read.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("world")
    ap.add_argument("--budget", type=int, default=300)
    ap.add_argument("--n", type=int, default=16, dest="n_residues")
    ap.add_argument("--model", default="claude-opus-4-7")
    ap.add_argument("--table", default="table_16.bin")
    ap.add_argument("--contacts", default="contacts_16.bin")
    ap.add_argument("--out", default="runs")
    ap.add_argument("--instructions", default="instructions.md")
    ap.add_argument("--seed-tag", default="", dest="seed_tag")
    args = ap.parse_args()
    run(args.world, n_residues=args.n_residues, budget=args.budget,
        model=args.model, out_dir=args.out, table_path=args.table,
        contacts_path=args.contacts, instructions_path=args.instructions,
        seed_tag=args.seed_tag)
