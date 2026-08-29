# 014 gradient_alpha1

Smooth gradient (linear interp) between two Dirichlet(1.0) endpoint compositions.

## Result: NEW BEST
- eval_01: **0.4066** (vs 0.3953 with Dirichlet(2.0) endpoints)
- All conditions better than alpha=2 baseline except b
- Many evals climbed to ~0.40

Stronger positional variation via wider endpoints helps. Try Dirichlet(0.5) next.
