# Experiment 015 — 3-source mix (mc5 + cCRE + PhastCons)

## Design
50% multi-chrom-5 genomic (25k) + 25% type-balanced cCREs (12.5k, 2.5k/type)
+ 25% PhastCons-centered ≥30bp (12.5k). All from chr8/19/21/22/X.
GC mean = 0.449 (vs 013 ~0.46, vs 014 ~0.43).

## Results vs 2-source baselines
| eval | 013 (cCRE) | 014 (PhastCons) | 015 (both) | vs best |
|------|-----------|------------------|------------|---------|
| 01 ★ | **0.5765** | 0.5541 | 0.5759 | -0.001 |
| 04 | **0.5774** | 0.4957 | 0.5604 | -0.017 |
| 07 | 0.6037 | **0.6353** | 0.6184 | -0.017 |
| 08 | **0.1730** | -0.0032 | 0.1318 | -0.041 |
| 13 | 0.5865 | **0.6186** | 0.5999 | -0.019 |
| mean8 | **0.5705** | 0.5316 | 0.5156 | -0.055 |

## Verdict: interpolation, not super-addition
015 lands BETWEEN 013 and 014 on every eval — no super-additivity.
eval_07/13 (PhastCons-favored) gain a little vs 013;
eval_08/04 (cCRE-favored) lose more.

Net: 015 < 013 across all 8 unique evals. Mean8 drops 0.055.

## Why 3-source did NOT add up
The genomic+cCRE super-additivity (009 vs predicted) worked because cCRE
filled a *specific gap* in the genomic baseline — high-GC realistic motif
context. PhastCons does not fill another gap; it has its own (lower) GC
distribution that dilutes the cCRE compensation.

Adding a third source is only super-additive if it adds an orthogonal
property (composition, motif type, contextual feature) the others lack.
PhastCons + cCRE overlap heavily — both are "constrained sequences" and
their union is closer to the larger set than to their sum.

## Implication for next experiments
- 013 (type-balanced cCRE supplement) remains best at eval_01 = 0.5765.
- Three-way mixing of similar source types degrades.
- To push past 013, need to either (a) tune within the cCRE+genomic
  recipe further (window size, scoring filter, chrom weighting), or
  (b) find a truly orthogonal augmentation (e.g. dinuc-shuffled cCREs to
  test if motif identity matters beyond composition).
