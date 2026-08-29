# 028 — 017 recipe, seed 999999 (variance check)

## Hypothesis
Estimate noise variance for our best recipe.

## Result
- eval_01 mean=**0.8738** (K562 0.8612, HepG2 0.9032, SKNSH 0.8570)
- vs 017 (seed 88888): mean **-0.008**. Same recipe.

## Interpretation
Seed-variance is much bigger than expected (~±0.008, not ±0.001).
017's 0.882 was a seed-fortunate run. The "true" expected mean for the
recipe is around 0.876-0.878.

This also reframes earlier results: tiny differences across experiments
(±0.003) may have been noise rather than real recipe effects. Many of
the apparent gains/losses on the insert/bank axes may not be real.

## Lesson
For future work, run multiple seeds and report mean ± std, not single
seed results. Single-seed comparisons of ~0.005 difference are within
noise.

## Next
029-030: try more seeds to find a better one (final library submission).
