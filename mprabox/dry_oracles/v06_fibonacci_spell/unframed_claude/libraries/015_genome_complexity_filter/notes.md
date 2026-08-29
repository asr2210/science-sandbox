# Experiment 015: Low-complexity filtered genome random

## Plan
Take top 75% by 6-mer Shannon entropy from random genome windows.
Drops repetitive / simple-repeat regions. Should boost per-sequence
information content.

## Result
- eval_01 mean_r = **0.1313** — WORSE than unfiltered (~0.135 expected)
- K562 r dropped (0.038 → 0.028)

## Implication
Low-complexity regions ARE informative for the model. Filtering them
out makes my library distributionally different from test sets, hurting
correlation. The test set likely includes natural-distribution sequences
(repeats and all).

## Theory update
T13: The optimum is NATURAL sampling distribution, including repeats.
Any deliberate filter (high entropy, accessibility, conservation,
single-cell-type) shifts away from optimum.

## Next
Try deterministic tiling (proper this time, balanced per-chrom by length).
Removes sampling noise. May give modest improvement if seed-variance is
the main remaining lever.
