# 030_hard_adjacent_negatives

## Design
5K cCREs x 8 WIDER tiles = 40K positives
+ 2.5K "adjacent" non-cCRE regions x 4 narrow = 10K negatives
= 50K. Adjacent = midpoint 600-2000bp from nearest cCRE.

Compared to 028 (negatives >2000bp from cCRE), tests whether
HARDER discrimination boundary lifts K562 further.

## Result
                eval_01  K562    HepG2   SKNSH
028 far neg:    0.3229   0.148   0.203   0.618  <- best
030 adj neg:    0.3223   0.146   0.202   0.619

Parity within noise (-0.0006). K562 bump slightly smaller
(0.146 vs 0.148). HepG2 and SKNSH unchanged.

## Interpretation
The K562 bump does NOT scale with negative difficulty. Easy
negatives (far intergenic) provide a clean enough contrast
signal. Hard negatives (adjacent flanking) carry similar
information content but no extra benefit.

This suggests the K562 bump uses BROAD intergenic features
(repeat density, large-scale GC, etc.) that are similar across
near-flanking and far-intergenic non-cCRE regions. The model is
not learning fine boundary detection — it is learning a
"functional vs. non-functional" classifier at coarse resolution.

## Final theory T20 (refined)
- 2 capacity pools:
  * IDENTITY/CONTEXT (wider tiles, RC). Lifts HepG2 + SKNSH.
  * DISCRIMINATION (paired non-cCRE neg). Lifts K562 + HepG2.
- HepG2 benefits from either; K562 needs discrimination; SKNSH
  needs identity coverage.
- Cross-pool stacking at ~20% neg fraction is the optimum
  (028: +0.0048 vs narrow baseline).
- Same-pool stacking has diminishing returns.
- Negative type matters: REAL intergenic > shuffled (which has
  no intergenic features). Adjacent flanking ≈ far intergenic.
- All non-mean_r levers (motif insertion, sat-mut, top-filtering,
  multi-source) cost capacity without adding skills.

## Best library: 028
5K cCREs x 8 WIDER (+/-400bp) tiles + 2.5K non-cCRE x 4 narrow
tiles = 50K. mean_r = 0.3229 (vs 0.3181 narrow baseline).
