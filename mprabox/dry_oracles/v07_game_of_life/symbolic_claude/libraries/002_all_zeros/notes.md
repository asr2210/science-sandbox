# 002 — All-zero constant strings

50,000 copies of "00...0" (length 200).

## Results
All evals: **NaN**.

## Interpretation
- Score is computed per-string (or per-string then averaged) with a correlation-like metric.
- Constant string has zero variance → correlation undefined → NaN.
- This rules out pure population-level scoring.
- The "r" in mean_r likely stands for Pearson correlation.

## Implication for future experiments
**Every sequence must have non-zero variance** across positions. Pure constants are unusable.
Safe minimum: at least one position must differ from the rest.
