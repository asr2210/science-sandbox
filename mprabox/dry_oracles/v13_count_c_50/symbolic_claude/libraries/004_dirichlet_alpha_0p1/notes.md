# 004 dirichlet_alpha_0p1

Same as exp 003 but with Dirichlet(0.1) — more extreme compositions.

## Result
- eval_01: **0.2816** (vs 0.3604 at alpha=0.5)  — DECREASED
- Most evals decreased compared to alpha=0.5
- eval_08: 0.1453 (still bad, lower than uniform random's 0.5795)

## Interpretation
Too-extreme compositions hurt. Sequences with ~95% one character
likely fall outside predictor training distribution → predictions
become noisy → correlation drops.

Sweet spot for composition variance lies between alpha=0.1 and alpha=∞.
alpha=0.5 best so far. Next: try alpha=0.3 or alpha=1.0 to bracket.
