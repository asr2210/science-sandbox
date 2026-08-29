# Exp 003 — per-sequence Dirichlet composition (alpha=0.5)

## Design
50,000 sequences, each with its own Dirichlet(0.5) composition profile.
Sampled i.i.d. with per-sequence composition.

## Result
eval_01 mean_r = 0.1118 (vs baseline 0.1272) — **slightly worse**.
condition_c dropped from 0.39 → 0.32 across most evals.
condition_a/b inched up a bit (from ~0 to ~0.01-0.03).

## Interpretation
Strongly biased compositions REDUCE the active condition (c). This
suggests the hidden scorer rewards either:
- relatively balanced composition (close to 25/25/25/25), OR
- positional / motif structure rather than gross composition.

Composition variance is *not* the lever. The baseline (uniform random)
already has near-balanced compositions and gives a stronger c-signal.

## Next direction
Test STRUCTURE separately from composition: e.g., sequences with
forced-balanced composition (exactly 50/50/50/50) but random ordering.
That isolates the structural / ordering effect.
