# 005 — Random genomic from chr19 + chr22

## What I tested
50k 200bp windows randomly sampled across chr19 + chr22 (97M valid
positions). Random orientation. Seed=42.

## Result
- eval_01 = **0.1325** (003 chr22-only: 0.1341)
- mean of evals = 0.1283 (003: 0.1281)
- K562: 0.034 (003: 0.037)
- HepG2: 0.167 (003: 0.169)
- SK-N-SH: 0.197 (003: 0.196)

## What this means
Adding chr19 to chr22 makes essentially NO difference. The random
genomic plateau is robust. Multi-chromosome diversity doesn't help
because chromosomes have similar global sequence-distribution
properties for random tile sampling.

## Theory update
Random genomic is a stable plateau at ~0.13. To break through, the
library design must change qualitatively, not quantitatively. Pure
content from the natural distribution is well-covered by ~50k random
tiles from a single chromosome.

## What to try next
006: combine genomic context + explicit motif augmentation. Take chr22
random windows and embed 2 random TF motifs per sequence. Tests if
adding motif signal on top of natural context boosts K562 (currently
0.034) without sacrificing the other cell types.
