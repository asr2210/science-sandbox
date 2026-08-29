# 020_extreme_variance_mix

7 sources × 7,200 each, then truncated to 50k.
Builds on 019 by adding chrY + chromHMM Het+Quies + pure PLS as extreme poles.

## Result
eval_01: 0.6822 — slight drop from 019 (0.6895)
eval_07: 0.7628 — tiny gain over 019 (0.7615)
eval_13: 0.7593 — gain over 019 (0.7549)
GC mean=0.455 std=0.122 min=0.000 max=0.925 (wider than 019)

## Interpretation: variance has a ceiling for eval_01
Wider GC range, but eval_01 went DOWN. chrY contains heterochromatin and
satellite repeats. K562 chromHMM Quies/Het regions are largely "dead"
genome. These likely fall OUTSIDE the predictor's training distribution
(probably MPRA-tested DNA, mostly euchromatic).

Refined hypothesis: variance helps IF added sequences remain within the
predictor's training distribution. Adding heterochromatin/satellite
sequences moves outside it and behaves like random — variance grows but
mutual information with target drops.

eval_07/13 went up slightly because those metrics may be more sensitive
to compositional variance, less to motif-level signal.

## Next
Try a mix that maximizes variance WITHIN euchromatic, regulatory-element
sequences. Drop chrY and chromHMM Het. Use cCRE PLS (very GC) + cCRE dELS
+ chr22 + chr19 + AT-rich euchromatin (whole genome ex chr19/22 chrM/Y).
