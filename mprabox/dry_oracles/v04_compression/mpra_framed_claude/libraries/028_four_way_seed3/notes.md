# 028_four_way_seed3 — notes

## Design
exp 011 design (4-way: 20K nat + 15K cCRE off + 10K DHS + 5K mouse) with SEED=3.

## Result
- eval_01 = 0.5005
- 4-way 4-seed mean (011/014/027/028): **0.4991** (0.5012, 0.4971, 0.4976, 0.5005)
- 4-way SD: 0.0021

## Interpretation
4th seed lands almost exactly on prior mean. 4-way design is robustly
~0.499 with SEM ~0.0010 (n=4).

## Comparison so far (4 seeds each)
| design | mean | sd | seeds |
|--------|------|----|-------|
| 4-way  | 0.4991 | 0.0021 | 0.5012, 0.4971, 0.4976, 0.5005 |
| 6-way  | (need 029) | | 0.5025, 0.5027, 0.4959 |

## Next test
exp 029: 6-way seed=3, complete the matched 4-seed comparison.
