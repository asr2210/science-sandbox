# 017_perposition_bias

## Hypothesis
Each position has one of {A,C,G,T} favored at 35% (others at 21.67%), favored base rotating every position. Library marginal exactly 0.25 each; per-seq stats nearly identical to random uniform.

Tests whether the eval is sensitive to per-position structure when summary stats match. If yes, a new lever; if no, the eval depends purely on per-seq summary stats.

## Result
- **eval_01 mean_r = 0.3975** (K562=0.6196, HepG2=0.4341, SKNSH=0.1389)
- Statistically tied with random uniform (0.3981, noise floor 0.001).

## Interpretation
Per-position structure is INVISIBLE to the eval. T7 strongly confirmed: the eval depends on per-sequence summary statistics (per-seq base counts and similar), not on per-position structure. Library uniformity is achieved both ways.

This rules out per-position bias as a lever.

## Summary of lever map after 17 experiments

**Levers that affect score:**
- Per-base count variance: STEEP cliff between 0 (012=0.024) and binomial 6 (001=0.398), partial recovery at σ=1.3 (016=0.186)
- Per-seq GC variance >0.10: smooth decline (005 σ=0.23 → 0.365; 004 σ=0.30 → 0.340)
- Real DNA content (002, 003 → 0.393): mild penalty for deviation from random uniform marginals
- Motifs (008 → 0.385): moderate penalty
- Complexity bias (007 no-runs → 0.375): moderate penalty
- Markov repeat bias (010 → 0.389): mild penalty
- Mixing (013 → 0.389): mild penalty

**Levers that DON'T affect score:**
- Per-seq GC variance in [0.010, 0.082]: plateau at 0.398
- Per-position structure with library-uniform marginals (017 → 0.398)
- Library uniqueness (011 duplicates → 0.392, only 0.006 below — modest effect)
- Random seed (009 → 0.397, noise floor 0.001)

## Best score so far
014 (per-seq GC σ=0.075) = 0.3989 ≈ random uniform 0.3981 (within noise).

## Next
- 018: per-seq GC σ=0.10 — boundary mapping of upper plateau edge
- 019-025: try more exotic levers (dinuc structure, k-mer enrichment, rejection-sampled "ideal")
- 028-030: final submission variants
