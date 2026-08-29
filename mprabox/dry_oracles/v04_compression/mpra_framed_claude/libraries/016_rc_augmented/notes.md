# 016_rc_augmented — notes

## Design
25K base (exp 011 ratios scaled to 25K) + 25K reverse-complements = 50K.

## Result
- eval_01 = 0.4961 (vs exp 011 = 0.5012; Δ = -0.0051)
- All evals slightly below 011 by 0.002-0.007
- eval_08 = 0.0978 (unchanged)
- Time: 28s

## Interpretation
RC augmentation does not help and slightly hurts. Two interpretations
consistent with the data:
1. Model is already RC-equivariant (or close to it). Adding RCs doubles
   redundant supervision; halves unique sequence diversity. Net loss.
2. The plateau is set by motif vocabulary the model sees, and 25K unique
   sources have less vocabulary than 50K unique.

Either way: don't substitute augmentation for unique content.

## Implication
Other augmentations (small shifts, dinuc-preserved noise) likely also
neutral-to-negative. **Information bottleneck is sequence content, not
example count.**

## Next test
Motif-rich natural windows. Pick natural human windows that score
highest on JASPAR motif content (using PWM matching). Hypothesis:
denser motif exposure per training step, within natural context.
This is curation within natural rather than substituting natural for
regulatory atlases.
