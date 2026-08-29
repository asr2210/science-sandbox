# 001 — random uniform DNA

## Design
50,000 sequences of length 200, each base drawn iid uniform from {A,C,G,T} with seed=0.

## Headline numbers
- eval_01 mean_r = **0.5177**
- mean_r across 14 evals: 0.474–0.525 (eval_08 is lowest)
- K562 r ≈ 0.99 in nearly every eval — random DNA models K562 activity almost perfectly
- HepG2 r ≈ 0.42–0.58
- SK-N-SH r ≈ 0 in every eval (essentially noise)
- prepare.py: 35 s eval, 1m18s wall total

## What this tells me
- The MPRA activity in K562 (at least as it manifests on the held-out evaluation sets) is **almost entirely predictable from sequence composition** — a model trained on random DNA learns K562 with r≈0.99.
- HepG2 is partly composition-driven (r ≈ 0.55).
- SK-N-SH activity is NOT composition-driven — a composition-only model has zero predictive power for it. So SK-N-SH activity in the eval sets comes from regulatory features that random DNA does not contain.
- This means the floor mean_r is much higher than I expected (0.52, not <0.2). Beating this baseline requires teaching the model regulatory features that lift SK-N-SH and the harder portion of HepG2.

## Why eval_08 is lower
eval_08 has lower HepG2 (0.42 vs ~0.57) and lower K562 (0.992 vs 0.995). Maybe a held-out set whose activity is less composition-dominated. Worth watching across experiments.
