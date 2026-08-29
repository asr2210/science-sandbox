# 008_dhs_ccre_functional_filtered

## What I tested
The 003 winning recipe (25K mean_signal-weighted + 25K numsamples-
weighted) restricted to DHS elements that overlap an ENCODE cCRE V3
class in {PLS, pELS, dELS}. CTCF-only, DNase-H3K4me3, and DHS without
any cCRE overlap were excluded.

Filtered pool: 1,246,568 elements (35% of 3.59M DHS).

## Result — within-noise tie with 003
| metric   | 008    | 003 (best) | Δ      |
|----------|--------|------------|--------|
| eval_01  | 0.7269 | 0.7327     | -0.006 |
| eval_07  | 0.7419 | 0.7618     | -0.020 |
| eval_08  | 0.7021 | 0.6984     | +0.004 |
| eval_13  | 0.7248 | 0.7469     | -0.022 |
| cross-14 | 0.7671 | 0.7735     | -0.006 |

Per-seed eval_01: 0.6935 / 0.7301 / 0.7572 (std ≈ 0.026 — wide,
matching the 001 noise floor).

Pattern: gains on eval_08 (+0.004), losses on eval_07/13 (-0.020 each).
Same shape as 002 (breadth-only) vs 001 (signal-only) — losing
cell-type-specific signal but gaining slightly on whatever eval_08 is.

## Why it didn't help
Two reasons:

1. **The mean_signal weight already implicitly selects functional
   elements.** Within the 003 pool, a high-signal DHS is overwhelmingly
   already a cCRE PLS/pELS/dELS — the cCRE label is correlated with
   the weights, so filtering doesn't change the high-weight tail much.
   It only removes elements from the low-weight tail (which the
   weighted draw was already deprioritizing).

2. **CTCF-only and DNase-H3K4me3 elements (excluded) carry useful
   regulatory information.** CTCF-only elements encode insulator/
   architectural grammar that the model uses; removing them costs us
   small but real signal on cell-type-specific evals (07, 13).

## Implication for next experiments
- ENCODE cCRE class is NOT an orthogonal quality axis to mean_signal
  + numsamples for this task. The information overlaps.
- The 003 recipe has saturated single-axis tweaks. Next frontier needs
  a STRUCTURALLY different lever — not "different way to weight
  elements" but "different way to use elements" or "axis from a
  different data type."
- Candidates: multi-window per element (data augmentation), TF-binding-
  density weighting, evolutionary turnover (cross-species DHS rather
  than phyloP), motif-content rich filter.
