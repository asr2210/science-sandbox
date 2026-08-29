# 002 — single-char buckets

- 12500 each of "0"*200, "1"*200, "2"*200, "3"*200.
- Result: condition_a = NaN for every eval; mean_r = NaN.
- Stderr: `ConstantInputWarning: An input array is constant; the
  correlation coefficient is not defined` × 14 (once per eval).
- HUGE INSIGHT: scoring uses Pearson/Spearman correlation. condition_a
  is the correlation-based metric; conditions b,c still work (non-corr).
- Practical implication: our strings must produce *variance* in
  whatever feature the scorer extracts. Pure repetition is dead.
- condition_b/c are non-NaN, so we have residual info.

## Useful skill
Created `skills/scoring_format.md` summarising the discovery.
