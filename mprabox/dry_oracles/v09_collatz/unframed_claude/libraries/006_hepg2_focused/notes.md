# 006 — HepG2-focused (weighted HNF4/HNF1/FOXA1)

**Hypothesis**: weighting HNF4/HNF1/FOXA1 more heavily will push HepG2_r above 002's +0.04.

**Design**: same density 6, but biased panel: HNF4 x3, HNF1 x3, FOXA1 x2, others base weight 0.5-1.5. Added FOXA1 (TGTTTGC) as new motif.

**Result**: eval_01 = **0.2237** (DOWN). HepG2_r = -0.080 (back to baseline negative).

**Interpretation**: stacking HepG2-specific motifs HURTS HepG2 score. Two candidate causes:
  (a) FOXA1 motif TGTTTGC is too short/promiscuous — actively bad
  (b) Over-representing HNF4/HNF1 (avg 1.5/seq each) flips the model's read

This contradicts naive "more HepG2 motifs → more HepG2 activity." Suggests **motif diversity matters more than dose**.

The 002 panel scored +0.038 with each motif appearing on average 0.6 times per sequence (uniform over 10). Going to 1.5 per motif of HepG2 ones reverses sign.

Theory T6 → T7: The model likely rewards a sequence that LOOKS LIKE A DIVERSE CIS-REGULATORY ELEMENT (multiple distinct TFBSs), not a concentrated cell-type-specific binder. Real enhancers are heterotypic — homotypic clusters can be repressive.

**Next**: probe K562 (test if K562 even responds to ANY motif). Then build a balanced sequence honoring diversity.
