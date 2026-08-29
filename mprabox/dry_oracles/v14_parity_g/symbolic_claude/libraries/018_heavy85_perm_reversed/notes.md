# 018 4 buckets HEAVY=0.85 with char permutation REVERSED (3,2,1,0)

eval_01: -0.0013 (b dropped from +0.0118 to -0.0016). Worse.
eval_04/09: +0.0050 (b=+0.0062, vs +0.0019 forward order). BETTER.
eval_13: b=+0.0099 (vs -0.0039 forward). BETTER.

CONFIRMS: char-bucket assignment ORDER matters. Different evals favor different
permutations. eval_01 prefers (0,1,2,3); eval_04/09 prefer (3,2,1,0).

Hypothesis: scorer extracts per-row scalar feature (likely "majority char index" or
similar). Correlation with target depends on whether target is monotone in same
direction.
