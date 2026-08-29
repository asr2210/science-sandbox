# 006 — Top-Activity Real MPRA Sequences

## Hypothesis
Selecting the most-active real MPRA sequences (top 50k by |K562_log2FC| +
|HepG2_log2FC| + |SKNSH_log2FC|) should maximise prediction variance and lift
SKNSH r above the 0.124 baseline from exp 005.

## Method
Sorted all 763k real 200bp sequences by sum of absolute log2FCs across cells.
Kept top 50k (score range 6.6 to 31.0).

## Result
- eval_01 mean_r = **0.3837** (WORSE than random real 0.4112, WORSE than random
  uniform 0.4200)
- K562: 0.524 (−0.023 vs random real)
- HepG2: 0.543 (−0.020 vs random real)
- SKNSH: 0.0835 (**−0.040 vs random real!**)

## Interpretation — theory update

Selecting top-activity sequences DECREASED SKNSH r. The "absolute activity"
direction is wrong. What helped in exp 005 was DIVERSITY of activity, not
extreme activity.

Why might extreme-activity sequences hurt?
- All sequences in this library are strong activators across all three cells.
  Predicted activities concentrate at the high end of the model's output range.
- The model variants may saturate at the top — both predict "high" but with
  small disagreements that dominate the Pearson r.
- Pearson r reflects how well the two predictions are linearly related across
  the library. If most predictions cluster in one corner, even small disagreements
  dominate and r drops.

The lever for SKNSH is *spread* of predicted activity, which requires sequences
with a wide range of true activities (mix of inactive and active), not just
the top tail.

Random uniform: predictions narrow but agreed → high r for K562/HepG2.
Random real: predictions wider (spread of activities) → SKNSH r jumps.
Top real: predictions narrow at the high end → SKNSH r drops back down.

## Next
Try a stratified or bimodal selection that explicitly maximises SPREAD of
SKNSH activity. Or simpler: mix random-uniform + random-real to keep K562/HepG2
agreement high while still getting the SKNSH variance boost from real sequences.
