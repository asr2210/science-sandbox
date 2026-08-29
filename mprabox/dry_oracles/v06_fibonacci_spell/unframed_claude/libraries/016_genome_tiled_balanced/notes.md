# Experiment 016: Balanced deterministic tiling

## Plan
Tile genome with chrom-proportional n_windows = round(50k * len/total),
random offset per chrom. Eliminates exp 007's chrom-order bias.

## Result
- eval_01 mean_r = **0.1349** — same as exp 014 random (0.1350)
- Tiling matches random within noise

## Implication
Sampling strategy (tile vs random) doesn't matter at this granularity.
50k windows over 3Gb is sparse enough that either gives near-max diversity.

## Next
Try reverse-complement augmentation: 50% of windows revcomp'd. Tests
whether the scorer model is strand-sensitive (DNA is double-stranded so
both strands carry information).
