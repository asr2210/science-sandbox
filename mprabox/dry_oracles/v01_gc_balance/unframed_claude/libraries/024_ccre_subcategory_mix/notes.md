# 024_ccre_subcategory_mix

022's recipe + split cCRE_all into explicit dELS, pELS, CTCF-only subcategories.

## Result
eval_01: 0.6916 — slightly below 022's 0.6930
GC mean=0.497 std=0.120

## Interpretation
Explicit subcategory split didn't help. cCRE_all already contains a
useful natural mix of labels; manual rebalancing slightly disturbed it.

022's recipe remains best.

## Next
- 025: replace whole_genome (least gene-dense) with more cCRE_all,
  keep the 022 structure otherwise.
