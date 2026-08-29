# 025 — chr20+chr22 5-bin GC strat

## What I tested
chr20+chr22 stride=50 windows, 5 quantile bins × 10k each = 50k.
Random orientation. Seed=42.

## Result — 5-bin worse than 10-bin on the larger pool
- eval_01 = 0.1368 (024 10-bin: 0.1376, -0.0008)
- mean of evals = 0.1298 (024: 0.1302)
- eval_03 = 0.1382, eval_12 = 0.1382

## Interpretation
With chr20+chr22's 2M candidate pool, 10-bin granularity is
slightly better than 5-bin. The "sweet spot" of bin count shifts
upward when pool size increases. With more candidates, finer bins
get enough samples to be informative.

## Theory update
Bin-count sweet spot scales with pool size:
- chr22-only (0.78M cands): peak at 10 bins (013)
- chr20+chr22 (2M cands): peak at 10 bins still (024); 5-bin is worse
  but tied with chr22 5-bin (012); maybe 15-20 bins now optimal

## What to try next
026: chr20+chr22 15-bin × 3,333 each. Tests if even finer
granularity now wins with the larger pool.
