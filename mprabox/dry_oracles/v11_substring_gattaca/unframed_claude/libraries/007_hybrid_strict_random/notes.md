# 007 — Hybrid 25k strict + 25k uniform random

## Hypothesis
Mixing strict (K562/HepG2 friendly) and random (SK-N-SH friendly) lets each
cell line find its preferred sub-population. Predict mean_r between the two
parents (~0.84), maybe slightly better.

## Setup
25,000 strict 50A/50C/50G/50T (shuffled) + 25,000 uniform random; interleaved
random order.

## Result
- eval_01 mean=**0.8780** (K562 0.8616, HepG2 0.9106, SKNSH 0.8619)
- BETTER than either parent. SK-N-SH 0.862 exceeds BOTH random (0.838) and
  strict (0.698) — non-linear gain.
- K562 0.862 ≈ midway between parents
- HepG2 0.911 nearly matches strict (0.913), so no real loss

## Interpretation
Pearson correlation is non-linear in subset composition. When two subsets
have different (prediction, truth) distributions, the combined correlation
can exceed either parent if (a) the per-subset slopes are aligned and
(b) the subsets' means differ on both axes. The combined cloud spans a
wider range, amplifying correlation.

This is a major axis: **multimodal libraries beat unimodal ones**. The
combined library generates a wider, more structured prediction distribution
that aligns with the wider, more structured test label distribution.

## Next
- 008: three-way mix (strict + random + motif). Tests if more diversity
  modes give further gains.
- 009-011: tune mix ratios to find optimum strict/random fraction.
- Long-term: explore other modes (Markov, anti-uniform, etc.) as additional
  subpopulations.
