# 029 — chr20-only 10-bin GC strat × 5k (diagnostic)

## What I tested
chr20-ONLY stride=50, 10 GC quantile bins × 5k. Same recipe as 013
(which used chr22) but with chr20.

## Result
- eval_01 = 0.1340 (013 chr22-only: 0.1375, -0.0035)
- mean = 0.1283
- eval_07 = 0.1344 (013: 0.1267, +0.008 — biggest jump)
- K562 in eval_07: **0.054** (highest K562 yet)
- eval_13 = 0.1355 (013: 0.1344, +0.001)

## Critical insight (T27)
**chr22 is uniquely valuable.** chr20-only is much worse on eval_01
than chr22-only. The eval distribution is closer to chr22's natural
compositional+sequence distribution than to chr20's.

024's gain over 013 comes from chr20 ADDING diversity to chr22's
strong base, not from chr20 being inherently better.

## Per-eval take
chr20 wins on eval_07 / K562 specifically. chr22 wins on
eval_01/02/03/05/06/11/12/14. This explains why 024 (chr22+chr20)
beats either alone on the broad mean — it captures chr22's primary
signal AND chr20's eval_07/K562 boost.

## What to try next
030: Final experiment. Verify 024's robustness with seed=43. If
030 ≈ 024 (within 0.001 on eval_01) → 024 is a stable design and
the ~0.137 plateau is real.
