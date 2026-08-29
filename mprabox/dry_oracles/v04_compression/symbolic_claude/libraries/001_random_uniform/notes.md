# 001 random uniform

Baseline: 50,000 random sequences from {0,1,2,3}, seed 42.

## Result
- eval_01: 0.2974
- Range across evals: 0.10 (eval_08) to 0.42 (eval_07)
- Time: 21.7s (very fast — model is small-ish or quantized)

## Observations
- `condition_a == condition_b` exactly in most eval sets
- `condition_c` differs slightly (sometimes up, sometimes down)
- Several eval sets have identical means (likely duplicates):
  - (01, 14): 0.2974
  - (02, 05): 0.2975
  - (03, 12): 0.3292
  - (04, 09): 0.2862
  - (06, 11): 0.3242
  - singletons: 07, 08, 10, 13
- Score range hints at correlation (mean_r) bounded in [0, 1]
- eval_08 is consistently the hardest task
- eval_07 is consistently the easiest

## Implications
- Random already gives ~0.30; need to figure out what pushes toward 1.0
- 14 evals likely = 7 unique tasks × 2 splits (5 pairs + 4 odd? — actually
  5 pairs + 4 singletons = 14, so likely 9 unique tasks)
