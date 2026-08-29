# 006 — High-density biological-style motifs (~40% coverage)

## Setup
Same motif set as exp 004 plus 4 more (8 total bio TF consensuses). Each
sequence gets ~12 motifs inserted non-overlapping (~80 bp coverage = 40%) in
uniform-random backgrounds. Mapping guess: 0,1,2,3 = A,C,G,T.

## Results
- eval_01 = 0.0195 (vs baseline 0.0420; Δ ≈ −0.022) — clear hit
- eval_08 = 0.0584 (vs baseline 0.1242; Δ ≈ −0.066) — biggest drop
- Per cell line in eval_01:
  - K562 = 0.0270 (≈ baseline 0.030)
  - HepG2 = 0.0489 (≈ baseline 0.055)
  - SKNSH = **−0.0174** (vs baseline 0.040; dropped a lot)

## Inference
- High motif density HURTS, especially on SKNSH (neuroblastoma)
- Pattern: K562/HepG2 remained near baseline; SKNSH crashed
- Motif insertion appears to push sequences in a direction that some
  cell-line predictors interpret as "different from natural" or anti-correlated
- After 3 motif experiments (003/004/006) at different densities, no motif
  strategy has beaten uniform random
- Conclusion: motif insertion is NOT the lever. Pivot direction.

## Next direction
Probe metric noise first (run a different uniform-random seed). If the metric
is very stable (low noise), I can be confident small changes are real. Then
try genome-like Markov chain sequences (dinucleotide structure but uniform
composition).
