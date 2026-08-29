# 001 — Uniform random baseline

Seeded uniform random over {0,1,2,3}. Establishes baseline for all 14 evals.

## Results
- mean_r ≈ 0.39 for most evals
- eval_08 stands out: 0.2753 (much lower baseline)
- eval_13 highest: 0.4054
- Runtime: 97.7s

## Structure of each eval
- mean_r = (condition_a + condition_b + condition_c) / 3 (verified)
- For all evals: a > b >> c
- condition_a ≈ 0.6, condition_b ≈ 0.43, condition_c ≈ 0.13
- condition_c is the bottleneck — improving c likely has biggest leverage

## Duplicate evals
These eval pairs return *identical* scores (not just close):
- 01 == 14
- 02 == 05
- 03 == 12
- 04 == 09
- 06 == 11
- 07, 08, 10, 13 are singletons

So really ~9 distinct eval signals. eval_01 is the primary target.

## Next steps
- Test if scoring is per-string or population-level
- Test compositional bias
