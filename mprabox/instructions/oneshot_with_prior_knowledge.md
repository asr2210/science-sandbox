# MPRA Library Design — One Shot (Informed)

## Objective
You are an autonomous, independent researcher designing a 50,000-sequence
library for a massively parallel reporter assay (MPRA), a high-throughput
experiment that measures how DNA sequences drive gene expression. The purpose
of this library is to train the best possible model of gene regulatory
activity. You can measure activity in K562, HepG2, and SK-N-SH, but the goal
is a model that captures regulatory grammar across ALL cell types — not just
these three. Design for general regulatory grammar, not for these specific
cell lines.

The library should be:
- Not specific to a set of tissues
- Not only functional elements
- Diverse in sequence space
- High training performance-to-size ratio

## How it works
You have **one commit**. Before you commit, you can do anything: read
literature, download and analyze data, write exploratory code, reason about
sequence properties, test hypotheses computationally. Take as long as you need.

When you are ready, commit your library. `prepare.py` will evaluate it
immediately and return your score. The run ends there — no further iterations.

Because you cannot iterate, invest heavily in understanding the problem before
designing.

## Lab Notebook
Keep a detailed lab notebook in `notebook.md`. Update it continuously
throughout your work — every time you have a new idea, run an analysis,
make a decision, or change direction, write it down immediately. Do not
save it for the end. It is part of the scientific record. Include:

- Your theory of what makes a good MPRA training library and why
- What sources of data or sequence types you considered and why you included
  or excluded each
- The specific design decisions you made and the reasoning behind them
- Any analyses you ran and what they told you
- What you would try next if you had another shot

Write this as if explaining your reasoning to a colleague who will read it
after the run. It should be detailed enough that someone could reconstruct
your thinking from scratch.

## What to produce
1. Write `notebook.md` documenting your reasoning and design decisions
2. Create a `library/` directory
3. Write `generate.py` that produces exactly 50,000 200bp sequences and saves
   them to `library/sequences.txt` (one per line, {A,C,G,T} only)
4. Run `python prepare.py library/sequences.txt`
5. `prepare.py` writes `library/result.json` with your scores
6. `git add -A && git commit -m "oneshot: mean_r=X.XXX" && git push`

## Rules
- `library/sequences.txt` must contain **exactly 50,000 lines**, each exactly
  200 characters from {A, C, G, T}
- You **cannot** modify `prepare.py` or any other existing files
- You **can** search the web, download data, install packages, write any code
- Store downloaded data and reference files in `data/`
- `prepare.py` is a black box — treat it like a wet lab assay. You hand it
  sequences; it returns measurements. Do not read or inspect it.
- You may call `prepare.py` **exactly once**. That call is your final
  submission. Do not use it as a probe or baseline — design first, then
  evaluate.

## Evaluation
`prepare.py` evaluates your library against 14 anonymous test sets (eval_01
through eval_14). You do not know what these sets contain. Each returns
mean_r, k562_r, hepg2_r, sknsh_r. Optimize across all of them — there is no
single primary metric.

The result is written to `library/result.json`.

---

## Prior Baselines

A reference of systematic baseline strategies (14 strategies × 7 library sizes
× 5 seeds, with the same harness you will use) is provided in
`../../strategies.md`. **Read it before designing your library.** Your goal is
to do better than the best strategy shown there.
