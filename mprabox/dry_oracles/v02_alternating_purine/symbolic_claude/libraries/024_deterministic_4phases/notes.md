# Exp 024 — deterministic 4-pattern library

## Result
NaN for all condition_c and mean_r. condition_a/b defined (0.03 range).
Per-cell freq = exactly 0.25 everywhere → constant input → Pearson NaN.

## CRITICAL INSIGHT
condition_c = Pearson between (library per-cell base frequencies) and
(eval reference per-cell freqs). When library per-cell is uniform (constant),
the input array has no variance → Pearson undefined.

This means condition_c is a per-cell-FREQUENCY correlation, NOT per-row.
It's also explanation for why condition_c is invariant to p magnitude:
Pearson is shape/scale invariant; what matters is the per-cell freq SHAPE
matching the eval's reference shape.

The 0.41 plateau = Pearson between our period-4-with-uniform-noise shape
and eval's reference shape. To increase c, we need to match the eval's
reference SHAPE more precisely — beyond just "template base = high".

## Next
Try asymmetric noise OPPOSITE to Exp 017: prev-in-cycle biased (0.7/0.05/0.05/0.2).
If c rises, eval has directional preference. Cheap directional test.
