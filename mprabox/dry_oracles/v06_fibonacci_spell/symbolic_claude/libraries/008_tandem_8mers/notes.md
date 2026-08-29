# 008 — Tandem 8-mer repeats

## Setup
50K sequences. Each = unique random 8-mer repeated 25x (200 chars).
Sampled 50K of 65536 possible 8-mers without replacement.

## Result
- eval_01 mean=0.1390 (k562=0.0410, hepg2=0.1710, sknsh=0.2050)
- Best so far. Up from 0.1349 (Dirichlet base).

## Interpretation
Pure tandem k-mer structures give the model a CLEAN signal to evaluate.
Both eval and ref models likely share TF-motif sensitivity, so when one
predicts "8-mer X is strong", the other agrees. This raises r.

Implication: ABSENCE of random noise (vs Dirichlet+random) actually
helps — the model has less ambiguity to score. Worth testing other k.
