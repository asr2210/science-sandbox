# 002 — 4-way single-character bias mix

50k = 4 groups of 12,500. Each group has 70% of one character, 10% each of others.

## Result
- eval_01: mean_r=0.1402 (vs 0.2399 baseline) → DROP of ~0.10
- All conditions dropped (a 0.14→0.04, b -0.05→-0.13, c 0.63→0.51)
- eval_08 also dropped (0.087→0.053)

## Interpretation
Strong single-character bias HURTS. Balance is preferred at the
per-sequence level. The drop in c (from 0.63 to 0.51) is biggest in
absolute terms — c may reward balanced composition.

Updated theory: scorer prefers sequences with balanced character
frequency. Random uniform is close to optimal on this axis. We should
preserve uniformity at the composition level and look for structural
improvements (motif placement, periodicity, diversity) within that.
