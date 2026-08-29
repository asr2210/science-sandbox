# 001 random_uniform

50,000 uniform random sequences (seed 42) from {0,1,2,3}, length 200.

## Result
eval_01 mean_r = 0.0013 (essentially zero)
All evals fall in range -0.004 to +0.002.

## Observations
- Random is the zero baseline; scorer can return both positive and negative values.
- Several evals return IDENTICAL values across all conditions:
  - eval_01 == eval_14
  - eval_02 == eval_05
  - eval_03 == eval_12
  - eval_04 == eval_09
  - eval_06 == eval_11
  → Effectively 9 unique evals: 01, 02, 03, 04, 06, 07, 08, 10, 13.
- Time: 27s scoring + ~30s data load = 56s wall clock.

## Next
Need to identify whether composition, motifs, or diversity drives score.
