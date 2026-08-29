# 022 — 3-mode: 25k strict + 12.5k pure rand + 12.5k insert-rand

## Hypothesis
Splitting random half into "with insert" and "without" adds productive
sub-cluster structure.

## Result
- eval_01 mean=**0.8714** (K562 0.8621, HepG2 0.9049, SKNSH 0.8471)
- vs 017: mean -0.011. SKNSH -0.025.

## Interpretation
Diluting the insert (half the random seqs without one) is strictly worse.
Insert needs to be in 100% of random half to maintain its cluster effect.

## Next
023: try inserts in strict half too, but with composition-preserving
balanced 8-mers.
