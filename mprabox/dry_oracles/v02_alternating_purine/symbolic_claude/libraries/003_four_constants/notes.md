# 003_four_constants

12,500 copies each of "0"*200, "1"*200, "2"*200, "3"*200. Library = 4 unique strings.

## Result
- All evals NaN.
- 7 ConstantInputWarning emitted (down from 41 in 002). So one input to most correlations
  is no longer constant, but somewhere else is still failing.

## Interpretation
- Going from 1 unique → 4 unique strings reduced the count of constant-input warnings,
  but result is still NaN. So either (a) the harness rejects libraries with too-few unique
  values, (b) it does deduplication and 4 distinct values give insufficient stats for some
  per-sample analysis, or (c) some intermediate quantity is still constant.
- Useless for scoring per se, but tells us the threshold for non-NaN is much higher than
  4 unique strings.

## Action
Run 004 with 50k *distinct* strings (random) but with varied single-character composition
per string — that decouples per-string structure (random) from per-library composition
spread.
