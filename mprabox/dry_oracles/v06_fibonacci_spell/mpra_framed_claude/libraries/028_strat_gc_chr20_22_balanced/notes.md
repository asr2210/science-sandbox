# 028 — chr20+chr22 10-bin × balanced 2.5k/2.5k per bin

## What I tested
10 GC quantile bins of combined chr20+chr22 pool. Per bin: forced
exactly 2,500 chr22 + 2,500 chr20 = 5k. Total 50k.

## Result — balanced HURTS vs natural-proportional 024
- eval_01 = 0.1356 (024: 0.1376, -0.002)
- mean = 0.1290 (024: 0.1302)

## Interpretation
024's natural-proportional sampling (chr22:chr20 varies by bin
based on candidate pool) outperforms balanced sampling. Forcing
extra chr22 into low/mid-GC bins (where chr22 is naturally scarce
in combined pool) reduced the per-bin diversity of CHR20-derived
windows AND added under-representative low-GC chr22 sequences.

024's "natural ratio" worked because:
1. Bins with abundant chr22 candidates → naturally rich chr22 share
2. Bins with scarce chr22 candidates → naturally chr20-dominated,
   which preserves compositional coverage without spurious chr22
   over-emphasis

## Theory update (T26)
Don't force chromosome ratios. Let the natural candidate pool
determine per-bin shares. The pool ratio is informative.

## What to try next
029: chr20-only 10-bin GC × 5k strat. Diagnostic: if chr20 alone
≈ 024 → chr20 carries all the signal and chr22 is redundant.
If chr20 alone < 013 → chr22 IS uniquely valuable.
