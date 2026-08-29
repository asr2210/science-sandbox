# 003 pure random

## Design
50,000 uniform random sequences over {0,1,2,3}, seed=3.

## Result
eval_01 = 0.5299 (k562=0.5300, hepg2=0.5767, sknsh=0.4831)

## Surprise
Pure random scored LOWER than exp 001's mixed library (0.5299 vs 0.5436).
Hepg2 dropped substantially (0.6301 → 0.5767), k562 went up.
So the "weird" strata in exp 001 (GC-rich, AT-rich, periodic, motif) HELPED
the overall score, particularly hepg2.

Per-eval pattern:
- Pure random: eval_07=0.5815, eval_13=0.5666, eval_08=0.1513
- Mixed (001): eval_07=0.5984, eval_13=0.5707, eval_08=0.1319
- Same ranking of evals; mixed wins on most, random wins on eval_08.
