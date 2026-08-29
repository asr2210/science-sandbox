# 017 uniform_marginal_43_57

c0, c1, c2 each sampled uniform on [43,57], c3=200-sum, rejected if out of range.
Different from 009's uniform-over-tuples (marginals are flat for c0/c1/c2).

Result: eval_01 mean_r = **0.8753** (slightly worse than 009's 0.8820).
- a: 0.839 (DOWN from 0.856)
- b: 0.909 (≈ same)
- c: 0.878 (≈ same)

Uniform marginal hurts a slightly. Bell-shaped marginal (concentrated near 50)
is slightly better for a. 009's natural distribution stays winner.
