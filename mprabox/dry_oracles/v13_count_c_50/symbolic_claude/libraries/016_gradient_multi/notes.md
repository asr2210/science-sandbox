# 016 gradient_multi

3-control-point piecewise linear gradient (Dirichlet(0.5) controls).

## Result
- eval_01: 0.3969 (vs 0.4078 with 2-point alpha=0.5)
- Slightly worse — adding a middle control point doesn't help

So linear two-point gradient is sufficient. Try pushing endpoint alpha lower.
