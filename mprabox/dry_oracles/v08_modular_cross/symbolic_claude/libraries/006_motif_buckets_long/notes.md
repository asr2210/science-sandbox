# 006 — Long motif buckets (motif length 100)

- Same 4-bucket arrangement as 005 but motif length 100 at pos 50-149.
- Result: mean_r decreased vs exp 005.
  - eval_01: 0.0029 (down from 0.0061)
  - eval_03: 0.0048 (down from 0.0074)
  - eval_10: 0.0052 (UP from 0.0039) — interesting
- Conclusion: bigger motif is worse for most evals.
- Possible reason: less background variance per string → weaker
  predictor variance within buckets; or motif-saturation hurts feature.
