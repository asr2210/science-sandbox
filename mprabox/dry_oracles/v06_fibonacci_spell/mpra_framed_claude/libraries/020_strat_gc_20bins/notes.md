# 020 — 20-bin GC stratification (2,500 per bin)

## What I tested
chr22 stride=50 candidates, sorted by GC, 20 quantile bins of
2,500 each. Random orientation. Seed=42.

## Result — over-stratification declines
- eval_01 = 0.1362 (013 10-bin: 0.1375; 012 5-bin: 0.1367)
- mean of evals = 0.1292 (013: 0.1298; 012: 0.1308)
- K562 = 0.044 (012: 0.038, +0.006)
- HepG2 = 0.170 (012: 0.174)

## Granularity sweep
| Bins | eval_01 | mean  |
|------|---------|-------|
|  5   | 0.1367  | 0.1308 |
| 10   | 0.1375  | 0.1298 | ← best eval_01
| 20   | 0.1362  | 0.1292 |

Peak at 10 bins. More bins → fewer samples per bin → noisier per-bin
coverage → worse generalization.

## Theory update
There's a sweet spot for granularity: ~10 bins × 5k each. Below
that, tails are underrepresented; above that, per-bin diversity
is insufficient. 

## What to try next
021: Complexity (trimer-entropy) stratification. Until now I've
explored GC and CpG as compositional axes. Complexity is a different
axis: low-complexity = repeats / homopolymers, high-complexity =
diverse. May expose a different ceiling.
