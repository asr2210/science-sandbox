# 011 more compositional strata

## Design
- 4 letter anchors × 1250 = 5000 (10%)
- 6 random strata × 7500: uniform, GC-rich, AT-rich, very-GC-rich,
  very-AT-rich, no-homopolymer

## Result
eval_01 = 0.5947 — NEW BEST (+0.026 over exp 009).
Improvements broad: eval_07 = 0.6591, eval_13 = 0.6303.

## Conclusion
Adding very-GC-rich [1,9,9,1] and very-AT-rich [9,1,1,9] strata
significantly helped. The wider compositional sweep stretches (f, g)
along the agreement line. Next: a finer GC-content sweep should help
further.
