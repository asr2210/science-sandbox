# 001_random_uniform

Baseline: 50,000 strings of length 200, uniform random over {0,1,2,3}, seed=42.

Result summary:
- eval_01 = 0.0408 (primary)
- Most evals 0.02–0.05
- eval_08 = 0.1222 (highest)
- eval_13 = 0.0191 (lowest)

Identified duplicate eval pairs (same r and conditions a/b/c):
01≡14, 02≡05, 03≡12, 04≡09, 06≡11.

This is our baseline to beat.
