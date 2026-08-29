# 015 — 4 buckets with bg enriched for bucket char (50% bias)

- Same as exp 005 but bg has 50% bucket char + 50/3% each of others.
- mean_r eval_01: -0.0019. WORSE.
- All evals went negative.
- Composition contrast across buckets actively hurts.
- Likely the predictor extracts a "non-motif feature" from background
  that's now bucket-correlated in a way that opposes the motif signal.
