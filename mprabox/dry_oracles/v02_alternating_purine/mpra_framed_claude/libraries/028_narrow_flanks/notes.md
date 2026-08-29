# Experiment 028 — narrow flank band (1800-2500bp)

## Design
- 013 ratio: 15K uniform + 5K CTCF + 5K DNH3 + 25K paired flanks
- ONLY change: flank distance band 1800-2500bp (vs 1500-3000)
  — narrower, centered on the sweet spot

## Result — mean_r 0.147 (worse than 013's 0.166)
- eval_06/11 dropped to 0.156 (down from 013's 0.218!)
- eval_07 = 0.177 (matches 013 exactly)
- eval_10 = 0.166 (up from 013's 0.151)
- eval_13 = 0.133 (similar)

## Interpretation
**Big surprise**: narrowing the band HURT eval_06/11 significantly,
even though 1800-2500 is INSIDE 013's 1500-3000. The variance in
flank distance (1500 to 3000) seems to be part of the signal —
the model learns "regulatory vs flank-at-various-distances" rather
than "regulatory vs flank-at-specific-distance".

Lesson: keep parameter ranges wide, not narrow. The diversity within
the band is itself informative.

## Next
029 = try a different direction. 013 with **RC augmentation**:
half of positives + half of flanks reverse-complemented. Tests if
strand-symmetry training helps.
