# 001 uniform_random

Baseline. 50,000 sequences, each char drawn uniformly i.i.d. from {0,1,2,3}.

eval_01 mean_r = 0.8526.

Observations:
- Multiple eval pairs return identical numbers (likely shared underlying metric)
- eval_08 condition_a is very low (0.55) - might be a property uniform random fails on
- eval_10 condition_a low (0.69)
- eval_07 condition_c low (0.68)
- eval_13 mean_r low (0.82)
