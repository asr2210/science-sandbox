# 001 — Uniform Random Baseline

50,000 i.i.d. uniform random strings over {0,1,2,3}, length 200.

## Results
All eval means within ±0.008 of zero. Scoring appears normalized so that
random input ≈ 0. To get positive score, structure is required.

## Key observation: eval pairs are identical
- eval_01 == eval_14
- eval_02 == eval_05
- eval_03 == eval_12
- eval_04 == eval_09
- eval_06 == eval_11

So there are ~9 distinct evaluators (5 paired + 4 unique: 07, 08, 10, 13).
Need to verify this pattern persists on non-random inputs.

## Notable variation despite zero mean
eval_07 condition_a = 0.0114, condition_b = -0.0125 (largest spread).
eval_10 mean = 0.008 (highest mean). These may have stronger preferences.
