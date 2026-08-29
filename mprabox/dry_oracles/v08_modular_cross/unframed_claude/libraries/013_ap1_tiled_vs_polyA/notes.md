# 013 — AP-1 tiled vs poly-A null

## Method
25k active: 8 AP-1 (TGAGTCA/TGACTCA) tiles spaced with random spacers in
200bp. 25k null: poly-A with random substitutions.

## Results (eval_01)
mean_r=-0.0012, K562=-0.0044, HepG2=+0.0039, SKNSH=-0.0032

## Lesson
- Minimum-within-class-variance design (near-identical active + near-
  identical null) did NOT beat baseline. eval_01 actually went slightly
  negative.
- eval_10 was the standout: K562=+0.0143, mean=+0.0057.
- poly-A null may be OUT OF DISTRIBUTION for the models, producing
  unpredictable random predictions that hurt correlation.
- Models may also be confused by repetitive AP-1 tiles vs natural
  enhancer spacing.

## Implication
"Both halves should look like reasonable DNA". Poly-A is too unnatural.
Pure motif tiling is also unnatural.

## Next (exp 014)
Try: non-overlapping motif placement (12 motifs at fixed-spacing
positions), cell-rotating motif identity (K562/HepG2/SKNSH covered per
sequence), matched-GC null. Should beat exp 008 because earlier code
had overlapping insertions degrading effective motif count.
