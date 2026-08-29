# 006 — HepG2-focused 50/50, matched GC=40%

## Method
25k active: GC=40% bg + dense HepG2 motifs (HNF1A, HNF4A, CEBPA, FOXA,
PPAR half-site). 25k null: plain GC=40%.

## Results (eval_01)
mean_r=-0.0030, K562=-0.0035, HepG2=+0.0034, SKNSH=-0.0088

## Lessons
- HepG2 motifs gave weaker signal than K562 motifs gave in exp 005.
  Best HepG2_r was +0.0077 in eval_10.
- K562 and SKNSH went NEGATIVE — AT-rich GC=40% background may be
  reducing variance for those cell-line models (everything looks
  similarly inactive to them, so noise dominates).
- mean_r worse than exp 005 because K562 and SKNSH dropped.

## Conclusion
HepG2 model is less motif-responsive than K562 model, OR my HepG2
motif panel is suboptimal. Either way, the "universal AT-rich" approach
doesn't lift HepG2 significantly and hurts the other cells.

## Next
- Try a UNIVERSAL motif library: strong broadly-active motifs (AP-1,
  SP1, NF-Y, CREB, ETS, MYC E-box) + cell-specific motifs interspersed,
  with matched GC null. Aim for all-three-cells positive.
- May also need: bigger motif density, longer or stronger consensus.
