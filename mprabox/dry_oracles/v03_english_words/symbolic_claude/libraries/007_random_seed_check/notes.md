# 007 — iid random different seed

iid random library, seed=1234567 (vs seed=42 in 001).

## Result
- eval_01: mean_r = 0.4239 (vs 0.4200 in 001) — within noise
- a = 0.5935, b = 0.6231, c = 0.0550

## Interpretation
**iid random gives ~0.42 ± 0.005 across seeds.** Stable target.

Seed luck isn't a major lever. To beat 0.42, need structural changes.
But every structural change tried so far HURTS. Need creative probes.

## Status: 7 of 30 used, 23 remaining

Best so far: iid random ~0.42 (either 001 or 007).
