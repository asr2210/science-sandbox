# 001 uniform random

Generated 50,000 iid uniform random strings over {0,1,2,3}, length 200.

## Key results
- eval_01 mean_r = 0.1451 (a=0.2806, b=0.0327, c=0.1219)
- eval_08 highest: 0.5795 (a=0.1779, b=0.7639, c=0.7966)
- eval_07 / eval_13 negative (~-0.12)
- Several evals appear identical (duplicates):
  - eval_01 == eval_14 (0.1451)
  - eval_02 == eval_05 (0.1437)
  - eval_03 == eval_12 (0.0919)
  - eval_04 == eval_09 (0.4001)
  - eval_06 == eval_11 (0.1340)
- mean_r = (a+b+c)/3 exactly (verified)
- Conditions a/b/c differ — they may be subsets or different metrics
