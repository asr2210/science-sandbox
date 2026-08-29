# Experiment 005 — 70% GC uniform random

## Hypothesis
T3 said the oracle is best on uniform-random-like distributions.
Test whether GC bias matters within the random-uniform family.
70% GC sequences should distinguish "GC matters" vs "uniform 50% is
the sweet spot".

## Method
Per-base iid sampling, P(G)=P(C)=0.35, P(A)=P(T)=0.15.

## Results
- eval_01: -0.0050 (random 50% GC: +0.0420)  → WORSE
- eval_08: -0.0221 (random 50% GC: +0.1237)  → DROPPED HARD
- HepG2 negative across the board
- Average: ~-0.006

## Interpretation
Both higher and lower GC than 50% reduce r. **Uniform 50% GC is a
local optimum on the composition axis.** This is consistent with
T3 (underlying model trained on uniform random) — the model is
best on uniform random.

This means composition isn't the lever; I need a different axis.

## Theory update
T3 stands. Composition tweaks within random-uniform family don't
help. The next likely levers:
- Per-sequence motif content (sparsely)
- Sequence STRUCTURE (positions, repeats, complementarity)
- DOWNLOAD real human sequences and test as a sanity check —
  if they're not better, then natural DNA isn't what the oracle wants.

## Next
EXP 6: real human genomic 200bp windows (download chr22, sample 50K
random windows). Decisive: if natural beats uniform → real DNA is
the path. If similar/worse → confirmed synthetic random model.
