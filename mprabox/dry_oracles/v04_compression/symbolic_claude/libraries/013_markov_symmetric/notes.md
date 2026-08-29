# 013 symmetric Markov (uniform stationary)

Doubly-stochastic transition (diag=0.4, off=0.2). Uniform stationary.

## Result
- eval_01 = 0.1914 (huge drop from 0.30)
- Even with NO composition skew, 1st-order correlations hurt severely.
- **Strong finding: ANY local correlation in sequences damages the score.**
- The learner is highly sensitive to deviations from iid.
