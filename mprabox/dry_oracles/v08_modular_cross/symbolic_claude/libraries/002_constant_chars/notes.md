# 002 — 4-way constant character probe

12,500 each of "0"*200, "1"*200, "2"*200, "3"*200.

## Results
mean_r and condition_a: NaN (correlation undefined)
condition_b and condition_c: non-NaN, small magnitudes

## Interpretation
ConstantInputWarning fired 14 times — once per eval. Correlation is being
computed somewhere in the pipeline; with only 4 unique strings (12,500 copies
each), some downstream array becomes constant.

condition_b/c are non-NaN aggregates (likely means, not correlations).
