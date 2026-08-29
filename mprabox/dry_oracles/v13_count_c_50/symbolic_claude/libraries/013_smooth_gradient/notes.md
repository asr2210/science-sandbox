# 013 smooth_gradient

Per-sequence linear interpolation between two Dirichlet(2.0) endpoint compositions.

## Result: NEW BEST
- eval_01: **0.3953** (vs 0.3917 alpha=2.0)
- condition_a improved 0.3958 → 0.4213
- condition_c improved 0.4077 → 0.4176
- condition_b slightly worse (0.3717 → 0.3470) but net positive

Smoothness of positional change matters — same endpoint distribution as two-block
but linear interpolation gives a slight win.

Next: try smooth gradient with MORE extreme endpoints (Dirichlet(1.0) or 0.5)
to see if stronger positional variation helps when transitions are smooth.
