# 001 — uniform random baseline

50,000 iid uniform random sequences over {0,1,2,3}, length 200.

## Result
- eval_01: mean_r=0.4200, a=0.5884, b=0.6187, c=0.0530
- mean_r = (a + b + c) / 3 (confirmed across all evals)

## Eval-set duplicates discovered
- eval_01 == eval_14
- eval_02 == eval_05
- eval_03 == eval_12
- eval_04 == eval_09
- eval_06 == eval_11

So 14 evals → ~9 unique. Plus eval_07, 08, 10, 13.

## Pattern across eval sets
- Most evals are near 0.42 (range ~0.419-0.427)
- eval_08 is consistently lower (~0.38 across all 3 conditions)
- Condition c is much lower than a, b across the board (~0.05 vs ~0.6)

## Interpretation
- Conditions a, b: roughly similar profile (a~0.59, b~0.62) — random sequences correlate substantially
- Condition c: very low for random — c is "harder" / requires different signal

## Time
- 34.4s reported by harness (out of 2m15s wall — overhead is loading)
