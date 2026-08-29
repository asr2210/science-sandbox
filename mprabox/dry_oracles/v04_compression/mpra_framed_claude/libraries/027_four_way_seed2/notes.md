# 027_four_way_seed2 — notes

## Design
exp 011 (4-way: 20K nat + 15K cCRE off + 10K DHS + 5K mouse) with SEED=2.

## Result
- eval_01 = 0.4976
- 4-way 3-seed mean (011/014/027): **0.4986** (seeds: 0.5012, 0.4971, 0.4976)
- 6-way 3-seed mean (024/025/026): **0.5004** (seeds: 0.5025, 0.5027, 0.4959)
- Δ between designs: +0.0018 (6-way > 4-way)
- SEM (n=3, sd~0.0022): 0.0013, so +0.0018 is ~1.4 SEM — marginal

## Interpretation
The 6-way design has a SMALL CONSISTENT EDGE (+0.002) over 4-way. Just
at statistical significance with n=3 seeds each. Need n=4 to firm up.

## Comparison summary
| design | n_seeds | mean | sd | seeds                  |
|--------|---------|------|----|------------------------|
| 4-way  | 3       | 0.4986 | 0.0022 | 0.5012, 0.4971, 0.4976 |
| 6-way  | 3       | 0.5004 | 0.0040 | 0.5025, 0.5027, 0.4959 |

6-way: higher mean BUT higher variance.

## Decision
Run 1 more of each (exp 028 = 4-way seed=3, exp 029 = 6-way seed=3) to
firm up. Then exp 030 picks the better-mean design.

## Next test
exp 028: 4-way design seed=3.
