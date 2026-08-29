# 009_offcenter_ccre_mix — notes

## Design
25K natural + 25K cCRE-containing windows where cCRE midpoint is at a
random offset within [25, 175] of the 200bp window. Same source as
exp 004 (centered) for the cCRE half.

## Result
- eval_01: 0.4956 (vs 0.4937 centered, +0.002)
- New best so far (just barely; within noise)
- Pattern identical to exp 004 across all evals
- eval_08 = 0.0917 (unchanged)

## Interpretation
Positional diversity helps marginally. Centering is not optimal, but
the gain is small (<0.5% relative). Likely the model has enough
translation-invariance baked in to its architecture that center-bias
matters little.

## Plateau still in effect
~0.49-0.50 ceiling on natural-based mixes. The gain from going off-center
is real but tiny.

## Next test
Try mouse genome as a source. Tests cross-species generalization:
- If 50K mouse natural ≈ 50K human natural (~0.48), grammar is universal.
- If mouse << human, grammar has human-specific components.
- If 25K human + 25K mouse > 0.49, multi-species mix breaks plateau.
