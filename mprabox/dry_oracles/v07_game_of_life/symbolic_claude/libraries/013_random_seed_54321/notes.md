# 013 — Random uniform seed=54321

Random seed scan #4.

## Result
- eval_01: 0.3973. cond_c: 0.1381.
- Better than seeds 42, 100, 12345.

## Interpretation
Trend continues: random uniform has small score variance across seeds, mostly
driven by cond_c (the bottleneck). Spread of ~±0.003.
