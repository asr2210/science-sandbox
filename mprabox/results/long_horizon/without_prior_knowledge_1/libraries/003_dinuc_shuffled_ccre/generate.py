"""Experiment 003 — dinucleotide-shuffled cCREs.

Take the same 50,000 cCRE-derived sequences as exp 002 and apply the
Altschul–Erickson dinucleotide-preserving shuffle to each sequence
independently. This preserves first-order Markov statistics
(GC content, dinucleotide frequencies, local CpG fraction) but
destroys all higher-order structure: TF motifs, motif spacings,
binding-site syntax.

Comparison logic:
- exp 001 (random uniform):       no biology, no composition match
- exp 002 (cCREs):                full biology + cCRE composition
- exp 003 (this, shuffled cCREs): cCRE composition, no motif syntax

If exp 003 ≈ exp 002 → composition explains the cCRE gain.
If exp 003 ≈ exp 001 → motif syntax explains the cCRE gain.
If exp 003 in between → both contribute.

Same per-seed sequence source as exp 002 to make this a clean
matched comparison: we re-run the exp 002 generator with the same
seeds, then shuffle the sequences using a *separate* RNG also seeded
deterministically (seed + 1000) so the comparison stays reproducible.
"""
from __future__ import annotations

import os
import sys
import numpy as np
from twobitreader import TwoBitFile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Re-import the cCRE generator's helpers to keep source sequences identical
EXP002_DIR = os.path.join(ROOT, "libraries", "002_encode_ccre")
sys.path.insert(0, EXP002_DIR)
from generate import (  # type: ignore  # noqa: E402
    load_ccres_by_class,
    generate as generate_ccre,
    GENOME_2BIT,
    N_SEQS,
    SEQ_LEN,
    ALPHABET,
)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def altschul_erickson_shuffle(seq: str, rng: np.random.Generator) -> str:
    """Dinucleotide-preserving shuffle (Altschul-Erickson Eulerian walk).

    Constructs a graph where each node is a nucleotide and each directed
    edge is a dinucleotide in the input sequence. A random Eulerian walk
    through this graph (starting at the original first nt and ending at
    the original last nt) yields a permutation with the same dinucleotide
    counts as the input.
    """
    n = len(seq)
    if n < 3:
        return seq

    first = seq[0]
    last = seq[-1]

    # adjacency: from each node, list of next-nt edges (dinucleotides)
    edges: dict[str, list[str]] = {nt: [] for nt in "ACGT"}
    for i in range(n - 1):
        edges[seq[i]].append(seq[i + 1])

    # Algorithm: shuffle each node's out-edge list, but ensure that for
    # every node u != last, the LAST edge in u's list points along a
    # spanning arborescence rooted at `last`. (Standard A-E algorithm.)
    for _ in range(50):  # try until we get a valid arborescence
        # randomize each adjacency list
        local_edges = {nt: list(es) for nt, es in edges.items()}
        for nt in "ACGT":
            rng.shuffle(local_edges[nt])

        # For each node u != last, move ONE edge that points (eventually
        # via back-following) toward `last` to the END of u's list. We
        # implement this by checking: do the "last edges" form an
        # arborescence rooted at `last`? Build the implied tree edge:
        # u --> last_edge_in_local_edges[u]. If for every u != last we
        # can reach `last`, it's an arborescence.
        last_edge: dict[str, str] = {}
        for nt in "ACGT":
            if nt == last:
                continue
            if not local_edges[nt]:
                continue
            last_edge[nt] = local_edges[nt][-1]

        # check reachability of `last` from every node with out-edges
        ok = True
        for nt in "ACGT":
            if nt == last or nt not in last_edge:
                continue
            cur = nt
            seen = set()
            while cur != last:
                if cur in seen:
                    ok = False
                    break
                seen.add(cur)
                if cur not in last_edge:
                    ok = False
                    break
                cur = last_edge[cur]
            if not ok:
                break
        if ok:
            break
    else:
        # Fallback: if 50 retries all failed, fall back to mononucleotide
        # shuffle (extremely unlikely for 200-bp sequences over ACGT).
        chars = list(seq)
        rng.shuffle(chars)
        return "".join(chars)

    # Walk the Eulerian trail
    out = [first]
    cur = first
    # convert lists to indices that we pop from front (cheap with reversed)
    iters = {nt: list(reversed(local_edges[nt])) for nt in "ACGT"}
    for _ in range(n - 1):
        if not iters[cur]:
            # ran out — happens only for malformed graphs; bail
            break
        nxt = iters[cur].pop()
        out.append(nxt)
        cur = nxt

    if len(out) != n:
        # extremely rare fallback
        chars = list(seq)
        rng.shuffle(chars)
        return "".join(chars)
    return "".join(out)


def write_seqs(seqs: list[str], path: str) -> None:
    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= ALPHABET for s in seqs)
    with open(path, "w") as f:
        f.write("\n".join(seqs) + "\n")


if __name__ == "__main__":
    print("loading cCRE BED...")
    by_class = load_ccres_by_class()
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)

    for seed in (0, 1, 2):
        print(f"seed {seed}: regenerating cCRE source sequences...")
        source_seqs = generate_ccre(seed, by_class, genome)
        print(f"  shuffling (dinucleotide-preserving)...")
        rng = np.random.default_rng(seed + 1000)
        shuffled = [altschul_erickson_shuffle(s, rng) for s in source_seqs]
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(shuffled, out)
        print(f"  wrote {out}: {len(shuffled)} seqs")
