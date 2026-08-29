# Exp 026 — gradient peak shape (soft peak)

## Result
eval_01 = 0.1147; condition_c = 0.3070. Worse than sharp-peak.

## Interpretation
Eval expects SHARP peak shape (1 base dominant, others equal).
Gradient peak (template 0.5, two adjacent 0.2, anti 0.1) does NOT
match. condition_c drops from 0.41 → 0.31.

Confirmed shape: per-position distribution should be "sharp single peak
+ flat tail". Our Exp 006 sharp-peak symmetric-noise design is at the
ceiling of this shape.

## Next
Test per-row noise direction variation while preserving library-wide
uniform noise shape. Hope: lifts condition_a/b without hurting c.
