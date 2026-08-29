# 030_final_submission — notes

## Design
6-way design (= exp 024): 20K nat + 8K cCRE + 7K DHS + 7K ChIP + 3K
FANTOM + 5K mouse, SEED=4. Canonical final submission library.

## Result
- eval_01 = **0.4974**
- A lower realization, on the bottom side of the plateau.

## Updated 5-seed comparison
| design | n | mean   | sd     | seeds                                  |
|--------|---|--------|--------|----------------------------------------|
| 4-way  | 4 | 0.4991 | 0.0021 | 0.5012, 0.4971, 0.4976, 0.5005         |
| 6-way  | 5 | 0.4998 | 0.0030 | 0.5025, 0.5027, 0.4959, 0.5003, 0.4974 |

Δ shrinks to +0.0007 (~0.4σ). Both designs are statistically
identical at this point.

## Per-eval results
- eval_01: 0.4974 (lower than 6-way mean)
- eval_07: 0.5889 (a bit below other 6-way seeds, all of which were 0.59+)
- eval_08: 0.1027 (stuck at ~0.10, as always)
- eval_13: 0.5894 (vs other 6-way seeds at 0.59+)

## Best-of-best submission candidates (single-realization eval_01)
| rank | exp | eval_01 |
|------|-----|---------|
| 1    | 025 | 0.5027  |
| 2    | 024 | 0.5025  |
| 3    | 011 | 0.5012  |
| 4    | 028 | 0.5005  |
| 5    | 029 | 0.5003  |
| 6    | 015 | 0.5002  |

If selecting on **single-best eval_01**: exp 025 (6-way seed=1).
If selecting on **design mean**: 6-way family (exp 024 series).

## Submission
This experiment (030) is the canonical "fresh seed" submission for
the 6-way design. The library is in `sequences_0.txt`.

## Recap of campaign
30 experiments total. The plateau at eval_01 ≈ 0.500 is structural for
noncoding regulatory atlases at this train budget. No curation strategy
(motif enrichment, conservation, TF balancing, GC stratification, RC
augmentation, variant perturbation) broke through it. The best designs
combine natural genomic background with mixed regulatory atlases
(cCRE/DHS/ChIP/FANTOM) at moderate fractions plus a small mouse
component.
