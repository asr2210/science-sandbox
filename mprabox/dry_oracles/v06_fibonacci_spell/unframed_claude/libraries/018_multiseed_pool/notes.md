# Experiment 018: Multi-seed pooled hg38 random

## Plan
4 seeds (101, 202, 303, 404), 12,500 hg38 random windows each, pooled
and shuffled. Tests pooling vs single-seed.

## Result
- eval_01 mean_r = **0.1357** — within noise band, like 014/016
- Multi-seed pooling does NOT add diversity at this scale
- Confirms: 50k random windows is already saturating the sampling

## Implication
The 0.1387 from exp 006 was a lucky single seed. Pooling 4 seeds
averages to ~0.135 just like a single typical seed. So pooling = no-op.
Genuine improvement requires departures from "uniform-random hg38":
either revcomp aug (017 was 0.1379, possibly noise), or domain knowledge
(test-distribution match).

## Next
Stack: pooled multi-seed + revcomp. Should test whether the small revcomp
gain in 017 was real (would show ~0.138-0.140) or noise (~0.135).
