# 001 — Uniform random baseline

## What
50,000 200bp sequences sampled uniformly from {A,C,G,T} per position
(rng seed 0).

## Why
Establish a floor for "no biology" against the 14 eval sets.

## Result
```
eval_01: mean=0.1185  K562=0.0064  HepG2=0.1571  SKNSH=0.1920
eval_08: mean=0.0587  K562=0.0066  HepG2=0.0671  SKNSH=0.1023
(other evals ~0.115-0.120 mean)
```
Runtime: 33s in prepare, 64s wall.

## Interpretation
- K562 ≈ 0 everywhere → random sequences have no correlation with K562.
- HepG2 and SKNSH show small but consistently POSITIVE r (~0.15, 0.19).
- eval_08 is an outlier — about half the magnitude of others. Likely a
  harder/different test set.
- The fact that random sequences give any positive r at all is interesting:
  prepare.py is probably running a fixed predictor that returns some
  per-sequence activity, and Pearson r is computed against a reference
  vector. With random inputs there's slight baseline correlation, perhaps
  from sequence composition alone.

## Next
Test whether known active motifs raise the score above this baseline.
