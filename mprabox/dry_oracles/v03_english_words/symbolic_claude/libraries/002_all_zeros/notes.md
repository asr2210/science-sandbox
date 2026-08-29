# 002 — 50K all-zero sequences

## Setup
50,000 identical copies of "0" * 200.

## Result
All NaN. Warning: `ConstantInputWarning: An input array is constant;
the correlation coefficient is not defined.`

## Interpretation
Metric is Pearson correlation. Constant predictions → undefined r.
**Diversity is REQUIRED.** Likely the metric is corr(predicted, true)
across the 50K sequences for each condition (a, b, c).

Time: 46.1s (vs 19.6s for random) — interesting; perhaps the model
takes a different code path for constant inputs.
