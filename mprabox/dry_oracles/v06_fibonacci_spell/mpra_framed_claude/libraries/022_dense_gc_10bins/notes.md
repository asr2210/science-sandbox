# 022 — Dense stride=10 + 10-bin GC strat

## What I tested
chr22 stride=10 sliding windows (3.9M candidates), position-dedup
at 50bp distance, then 10 GC quantile bins × 5,000 each. Random
orientation. Seed=42.

## Result — denser pool doesn't help
- eval_01 = 0.1363 (013: 0.1375, -0.001)
- mean of evals = 0.1290 (013: 0.1298)
- K562: 0.040 (013: ~0.044, -0.004)

## Interpretation
The 013 plateau (0.1375) was NOT due to limited candidate-pool size.
Stride=50's 78k per bin already gave enough diversity. Going denser
just shuffles which 5k are chosen and slightly worsens it.

## Theory update
Sampling-pool size is not the bottleneck. The plateau is structural
to the chr22-composition design space.

To break above 0.1375 I need either:
- compatible second chromosome (chr20/21 — similar GC to chr22)
- combined-axes design (013's granularity + 018's aug)
- synthetic-sequence generation matched to chr22 statistics

## What to try next
023: Combine 013's 10-bin strat with 018's dinuc-shuffle aug.
10 GC bins × 2,500 unique chr22 windows × 2 versions (real + dinuc-
shuffled) = 50k. Tests if finer granularity + augmentation
together beats either alone.
