# 002_all_zero

50,000 copies of "0"*200. Zero diversity.

## Result
- ALL eval values are **NaN**.
- scipy emitted `ConstantInputWarning: An input array is constant; the correlation coefficient
  is not defined.` 41 times.
- One warning seems to be missing from the full 14*3=42 set — possibly one condition uses a
  metric that doesn't need variance, or one condition fails earlier.

## What this tells us
- **The scoring metric is a correlation coefficient** (scipy `pearsonr` or `spearmanr` ⇒
  `ConstantInputWarning`).
- The score requires the 50k strings to produce non-constant per-string features. A
  constant library yields undefined r.
- This means the score isn't "is the string good in isolation" — it's "do the predictor's
  outputs across the library correlate with something".
- Implications for library design: diversity is mandatory, but more importantly the library
  must spread the predictor's outputs along the axis the "reference" varies on.

## Theory update
The scoring is something like `pearsonr(predictor(library), reference_signal(library))`
or `pearsonr(predictor_A(library), predictor_B(library))`. To maximize, we want library
diversity that *projects onto the axis both signals agree on*. Pure random gives a weak
correlation because variance is broadband; structured diversity that emphasizes the
"agreed axis" could do better.
