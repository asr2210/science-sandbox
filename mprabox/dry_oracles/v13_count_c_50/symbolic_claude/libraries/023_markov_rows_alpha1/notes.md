# 023 markov_rows_alpha1

Gradient (α=0.5 endpoints) + Markov weight 0.2 with Markov rows ~ Dirichlet(1.0).

## Result: NEW BEST
- eval_01: 0.4121 (vs 0.4115 at α=0.5 rows)

Marginal improvement. Smoother Markov rows = smoother transitions.
condition_a=0.4664, b=0.3542, c=0.4159

Try alpha=2.0 (even smoother) and alpha=0.3 (sharper) to map the curve.
