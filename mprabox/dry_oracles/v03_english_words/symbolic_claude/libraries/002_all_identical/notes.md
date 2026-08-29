# Exp 002: All identical sequences

## What
50,000 copies of `"0123" * 50` (length 200).

## Result
All evals returned NaN. Console warning: `ConstantInputWarning: An input array is
constant; the correlation coefficient is not defined.` from `eval/harness.py`.

## Interpretation
The scoring metric is Pearson correlation. When all 50k of our sequences are identical
(and the oracle gives identical predictions for them), correlation is undefined.

## Implications
- **The scorer correlates over the 50k sequences (NOT 50k → single score average).**
- We need DIVERSITY in our sequences to get any non-NaN score.
- Maximizing mean_r means maximizing the correlation between (whatever model is
  producing predictions) and (whatever target signal exists per sequence) over our
  submitted set.
- Random uniform already gets ~0.6 for K562/HepG2 (easy targets) and ~0.04 for SKNSH
  (hard target).
- To boost score, we want our 50k to span a wide range of "predicted activity" AND
  for that prediction to correlate with the (unknown) target. Stratified or designed
  diversity should help.

## Time
~2 minutes.
