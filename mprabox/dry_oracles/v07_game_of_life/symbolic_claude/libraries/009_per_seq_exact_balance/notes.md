# 009 — Per-sequence exact char balance

Each of 50k sequences is a permutation of [0]*50 + [1]*50 + [2]*50 + [3]*50. Per-seq
char count is EXACTLY 50 each.

## Result
- eval_01: 0.0436 (massive drop of 0.35 from random!)
- cond_c is negative on most evals.

## Interpretation
**Random's stochasticity in per-sequence composition is essential.** Removing
per-sequence variation (perfect balance) destroys the score.

## Theory update (major)
The scoring function rewards:
1. Per-position population uniformity (~25% each char)
2. NON-ZERO per-sequence composition variation across the population
3. Specific level of within-sequence randomness (independence across positions)

In exp 009, all sequences have identical char counts → per-channel COUNT std across
sequences = 0 → scores collapse to near zero (NOT NaN because mean per position is
still uniform with Poisson-like noise from random shuffling).

## Hypothesis: random is near-optimum
- Per-position uniform: ✓ (random achieves)
- Per-sequence variance: ✓ (Binomial(200, 0.25) per char)
- No structure (independence): ✓ (random satisfies)

Deviations in any direction HURT (bias, periodicity, template, exact balance, sub-alphabet).
Uniform random may be the local (or global) max for this scoring function.

## Next probes
- Test if SMALL bias hurts proportionally (exp 010)
- Test if dinucleotide structure matters (exp 011)
- Run replicate of best (uniform random) to confirm
- Submit final = uniform random
