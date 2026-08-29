# 001 — random baseline

## Method
- 50,000 sequences, 200bp each, uniform i.i.d. nucleotides, seed=42.

## Results
All 14 eval mean_r in the range [-0.003, +0.008]. Per-cell-line values
all in [-0.016, +0.014]. Essentially noise floor for the metric.

## Key observations
1. Random gives ~0 — strongly supports the metric being Pearson r (or
   another correlation-like statistic) against some hidden target.
2. **Duplicate evals**: several pairs return identical numbers:
   - 01 == 14
   - 02 == 05
   - 03 == 12
   - 04 == 09
   - 06 == 11
   Unique evals: {01,14}, {02,05}, {03,12}, {04,09}, {06,11},
   07, 08, 10, 13  →  effectively 9 distinct test sets.
3. mean_r equals the simple mean of (k562_r, hepg2_r, sknsh_r), so
   mean_r is the average of the three cell-line correlations.
4. Noise floor at n=50k is ~ 1/sqrt(50000) ≈ 0.0045; per-cell numbers
   are consistent with that.

## Implications for next experiments
- I need a SIGNAL strong enough to clear noise (~0.01+ to be confident).
- Random gives no signal → the scorer rewards information content, not
  the mere presence of sequences. Probably correlation between a model's
  prediction of regulatory activity and either a held-out target or
  another model's prediction.
- Strategy: produce libraries with **wide, predictable dynamic range** —
  obviously inactive (low-complexity, AT-only, etc.) mixed with
  obviously active (TF-motif-dense). If the metric correlates two
  predictors of activity, agreement is highest when there is a wide
  spread of activity levels.
