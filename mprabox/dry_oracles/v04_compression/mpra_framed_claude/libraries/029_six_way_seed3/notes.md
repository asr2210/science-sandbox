# 029_six_way_seed3 — notes

## Design
exp 024 design (6-way: 20K nat + 8K cCRE + 7K DHS + 7K ChIP + 3K FANTOM + 5K mouse) with SEED=3.

## Result
- eval_01 = 0.5003
- 6-way 4-seed mean (024/025/026/029): **0.5004** (0.5025, 0.5027, 0.4959, 0.5003)
- 6-way SD: 0.0032

## Final 4-seed comparison
| design | mean | sd | seeds |
|--------|------|----|-------|
| 4-way  | 0.4991 | 0.0021 | 0.5012, 0.4971, 0.4976, 0.5005 |
| 6-way  | 0.5004 | 0.0032 | 0.5025, 0.5027, 0.4959, 0.5003 |

Δ = +0.0013 (6-way > 4-way), pooled SEM ≈ 0.0019.
~0.7σ — NOT statistically significant. The earlier impression of a
real edge does not survive 4 seeds.

## Interpretation
The 6-way design is INDISTINGUISHABLE from 4-way at the plateau.
Both families average 0.499–0.500 with overlapping CIs. The "best
realization" (0.5027 from exp 025) is just the lucky upper tail.

## Strategic decision for exp 030
Pick one design as the final submission. Either family is equally
defensible. Choose **6-way (exp 024 design)** because:
1. Marginally higher mean (0.5004 vs 0.4991, +0.0013).
2. Higher single-realization ceiling (0.5027 max vs 0.5012 max).
3. Greater atlas diversity → more robust to unseen evaluation regimes.

exp 030: 6-way design with SEED=4 (a fresh untouched seed), as the
canonical final submission library.
