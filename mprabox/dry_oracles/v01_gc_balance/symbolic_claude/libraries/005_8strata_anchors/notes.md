# 005 8-strata anchors

## Design
8 strata × 6250 each:
A-D: 4 letter constants (all-0, all-1, all-2, all-3)
E: uniform random
F: GC-rich random
G: AT-rich random
H: 0123-periodic constant

## Result
eval_01 = 0.5627 (k562=0.5371, hepg2=0.6389, sknsh=0.5122)
Across all evals: improved over both exp 001 (0.5436) and exp 003 (0.5299).
Magnitude of improvement: ~+0.02 on most evals; eval_07 went +0.022.

## Interpretation
Adding more constant anchors (all-1, all-2, all-3) HELPED. This is
consistent with theory v3: each anchor contributes a high-weight (f, g)
point. If those points lie at extremes along the f-g regression line, they
stretch the cloud and raise r.

## Next
Exp 006: pure 4-letter constant library (only 4 distinct seqs). Tests if
the anchors alone drive most of the gain. With only 4 distinct points, the
Pearson r over the bag equals the r over those 4 points (replicate weight
cancels), so we directly read out how aligned the 4 letter-anchors are
in (f, g) space.
