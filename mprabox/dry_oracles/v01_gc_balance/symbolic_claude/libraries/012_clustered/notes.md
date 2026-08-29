# 012_clustered

## Setup
Same composition gradient as 009 but with chars SORTED within row (clustered)
then cyclically shifted by row-dependent offset.

## Results — CATASTROPHIC DROP
- eval_01: -0.0189 (009 was 0.6010)
- All evals collapse to near zero or negative.

## Interpretation
The model is POSITION-SENSITIVE. With random shuffle (009), per-position
distribution across the library is approximately uniform (since each row
is a random permutation of its composition). The model interprets this
correctly.

With sorted + shifted, position p of row i is determined deterministically
by (counts, shift_i). Even with shifts, the per-position distribution
across library is highly structured (not random) and the model's per-row
predictions become decoupled from composition.

## Important rule
**Always randomly shuffle chars within each row.** Don't impose intra-row
structure unless you've designed a careful row-correlated positional motif
plan.
