# 026 — chr20+chr22 15-bin GC strat (3333 per bin)

## What I tested
chr20+chr22 stride=50, 15 quantile bins × ~3333 each = 50k.

## Result — 15-bin much worse than 10-bin
- eval_01 = 0.1330 (024 10-bin: 0.1376, -0.005)
- mean of evals = 0.1278
- All evals dropped.

## Why
With 15 bins × 3333 per bin, the model doesn't get enough natural
diversity per bin. T22 (unique natural windows per bin matters)
strikes again: when per-bin sample count drops below ~5k, the
model's per-bin learning suffers.

The sweet spot is bins × per_bin ≥ ~5k per bin AND total = 50k.
For 50k/50_000 budget: 10 bins × 5k is optimal (and 5 bins × 10k
is close second).

## Theory update
The sweet spot is 5,000 samples per bin (roughly), regardless of pool
size. Going below hurts. Going above (fewer bins) loses tail
coverage.

## What to try next
027: chr20+chr21+chr22 triple-chromosome 10-bin × 5k. Tests if
chr21 adds further compatible diversity.
