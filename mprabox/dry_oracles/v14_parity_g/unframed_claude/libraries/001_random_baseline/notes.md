# 001 — Random uniform ACGT baseline

50K sequences, 200bp each, uniform iid base sampling. Seed=42.

## Result
mean_r ≈ -0.002 across all 14 eval sets (range -0.0064 to 0.0010).

## Interpretation
Random sequences give a floor of essentially zero correlation. This is consistent with the scoring being Pearson r against some target.

## Duplicate eval pairs (identical metrics)
- eval_01 == eval_14
- eval_02 == eval_05
- eval_03 == eval_12
- eval_04 == eval_09
- eval_06 == eval_11

So 14 evals → 9 unique conditions.
