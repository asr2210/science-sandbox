# 015 palindromes_mix

25k Watson-Crick palindromes (left half random, right half = reverse-complement
with 0↔3, 1↔2) + 25k random uniform.

## Result
eval_01 = -0.0006 (basically zero). eval_08 condition_c = +0.0084.

## Interpretation
Palindromic structure doesn't move eval_01. Might benefit eval_08 via condition_c.

Still: Dirichlet(0.5) is the best eval_01 strategy.
