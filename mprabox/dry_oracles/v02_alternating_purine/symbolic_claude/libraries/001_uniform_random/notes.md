# Exp 001 — uniform random baseline

## Design
50,000 i.i.d. uniform random strings of length 200 over {0,1,2,3}, seed=1.

## Result
eval_01 mean_r = 0.1272 (range across evals 0.05 – 0.15).

## Observations
- Conditions a and b are identical (or nearly so) in every eval.
- mean_r = (a + b + c) / 3 holds exactly across all evals.
- Condition c is the only one producing positive bias on random strings
  (~0.4 on most evals, 0.16 on eval_08).
- eval_08 is the lowest-scoring eval (mean=0.052) — likely stricter or
  different signal.

## Implications
- All scoring signal comes from condition_c above the noise floor; tuning
  for c will dominate mean_r.
- eval_01 == eval_14 == identical values, eval_02 == eval_05, etc. Several
  evals appear redundant (paired): 01/14, 02/05, 03/12, 06/11.
  Effectively maybe 8-9 unique evals.
- A baseline of 0.127 is what to beat for the primary metric.
