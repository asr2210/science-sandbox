# 006 pure 4-letter library

## Design
12500 copies of each of '0'*200, '1'*200, '2'*200, '3'*200.

## Result
NaN everywhere. ConstantInputWarning fired.

## Interpretation
With only 4 distinct seqs in the bag, AT LEAST ONE of (f, g) is constant
across {all-0, all-1, all-2, all-3}. So either the predictor f or the
ground-truth g (or both) is invariant to which single letter the sequence
contains.

This is a significant clue: the underlying predictor saturates or has a
default response to single-letter inputs (no internal complexity).

## Reconciling with exp 005 win
In exp 005 the 4 letter anchors WERE present and the score improved over
exp 001/003. But when isolated (006), they collapse to NaN. So the gain in
005 must come from how the anchors interact with the diverse strata —
likely by stretching the variable dimension while contributing to a single
point in the constant dimension.

Action: try dimer-repeat library to test if 2-character compositional
variety breaks the degeneracy.
