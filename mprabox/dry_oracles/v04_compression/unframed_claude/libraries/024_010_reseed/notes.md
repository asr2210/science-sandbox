# 024 — 010 reseed (noise floor test)

## Setup
EXACT same config as 010 but seed=424242 instead of 20260610.

## Results
eval_01 = 0.3106. exp 010 was 0.3644. Δ = **0.054**!

## Insight
**Critical finding**: seed variance for this config is much larger than
assumed (~0.03 std, ~0.05 swing). Confirmed in 027 (seed 99 → 0.3398).
So 3 seeds of identical config give 0.31, 0.34, 0.36. **exp 010's
0.3644 is at the lucky tail of a wide distribution.** Many "worse"
configs may actually be equivalent.

Implication: real differences between configs need to be > 0.05 on eval_01
to be confident. Most of my exp 011-023 deltas are within noise.
