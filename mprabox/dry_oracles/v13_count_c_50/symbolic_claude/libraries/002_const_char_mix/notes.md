# 002 const_char_mix

50000 sequences = 12500 copies each of "0"*200, "1"*200, "2"*200, "3"*200.

## Result: ALL NaN
- `ConstantInputWarning` from `eval/harness.py:111` shows metric is Pearson r
- a, b NaN for everything; c is 0 or NaN
- Only 4 unique sequences → many internal arrays go constant → undefined r

## Huge insight (theory revision)
- mean_r is mean of 3 Pearson correlations (a, b, c)
- The correlations are over arrays of length 50000 (or similar)
- Likely: corr(predictor1, predictor2) or corr(prediction, ground_truth) across sequences
- HIGH r requires high VARIANCE in per-sequence scores + good agreement
- Random uniform gives r ≈ 0.15 because variance is moderate

## New strategy
Maximize variance in whatever predictors care about (likely composition / motifs).
Library should span a wide range of activity values.
