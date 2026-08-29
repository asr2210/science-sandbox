# Experiment 012 — 64-motif pool

## Result
eval_01: 0.344 → **0.326** (DROP). Most evals slightly dropped.

## Interpretation
More diversity isn't strictly better. The additional 32 motifs (many longer, with IUPAC ambiguity codes that randomize each instance) diluted the signal from the original 32 high-quality motifs.

Possible mechanism: a pool of 32 "strong, short, canonical" motifs provides higher per-instance signal than a pool of 64 mixed-quality. Effective signal density drops when diluted with longer/ambiguous motifs.

## Next
Two paths:
1. Verify reproducibility of exp 011 (0.344) with different seed (rule out luck).
2. Push the 32-motif pool with different modifications (e.g., 2 motifs per seq).

Going with (1) first — if 0.344 is reproducible, then build on it. If it was a lucky seed, need to recalibrate.
