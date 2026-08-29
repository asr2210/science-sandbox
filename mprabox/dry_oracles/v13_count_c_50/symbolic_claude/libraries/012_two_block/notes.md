# 012 two_block

Each sequence = two halves with independent Dirichlet(2.0) compositions.

## Result
- eval_01: 0.3785 (below alpha=2's 0.3917)
- condition_a JUMPED to 0.4480, condition_b CRASHED to 0.2845
- eval_08: 0.3726 (jumped!) — two-block helps it a lot

## Interpretation
Predictor "a" likes positional composition variation; predictor "b" hates it.
Net negative for eval_01. There's a tradeoff between predictors.

Next: try SMOOTH positional gradient (interpolate between two compositions) so
adjacent positions have similar composition — might keep both a and b happy.
