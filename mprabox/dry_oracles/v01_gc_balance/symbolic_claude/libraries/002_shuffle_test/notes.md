# 002 shuffle test

## Design
Reused exp 001's 50,000 sequences but randomly permuted row order
(seed=2026).

## Result
ALL scores identical to exp 001 (to 4 decimals, with only 1 eval shifting
in the last digit due to floating-point order).

## Interpretation
**Row order does NOT matter.** The scoring function is a bag-of-sequences
statistic — order-invariant. This invalidates Theory v1 (per-row hidden
targets).

## Implication
The score must be a function of the *set* of 50k sequences. Likely forms:
- Aggregate: e.g., mean/median of a per-sequence quality score.
- Distributional: e.g., correlation between two model outputs across the
  empirical distribution of our seqs.
- Comparative: e.g., compare our bag's distribution to a hidden reference.

The "_r" suffix could mean (a) Pearson r between two latent per-sequence
outputs across our 50k seqs, or (b) just a naming convention for "reward".

## Next probe
Submit a fully constant library (all 50k seqs identical) to test:
- If "_r" is correlation between two latent outputs: constant inputs give
  constant outputs → r = NaN/0.
- If "_r" is aggregate quality: constant input gives some defined score.
