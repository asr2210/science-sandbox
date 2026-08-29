# 001_random_uniform

Baseline: 50,000 uniformly-random strings over {0,1,2,3}, seed 0.

## Result
- eval_01 mean_r = **0.1159**
- Most evals fall in [0.115, 0.137]
- eval_08 is much lower at 0.0517
- Wall time: 38.5s (prepare.py reports), real 1m25s

## Observations
- `mean_r = (condition_a + condition_b + condition_c) / 3` (confirmed on multiple evals)
- `condition_a == condition_b` *exactly* on all 14 evals. So a and b are very tightly coupled
  (perhaps two scoring tracks that coincide for random input, or just identical metrics).
- `condition_c` is consistently much higher (≈0.36) than a/b (≈0). The mean is dominated by c.
- Several eval pairs return *exactly* the same numbers:
  - eval_01 == eval_14
  - eval_02 == eval_05
  - eval_03 == eval_12
  - eval_04 == eval_09
  - eval_06 == eval_11
  - So 14 evals reduce to ≤10 unique ones (likely 9 + eval_08-outlier).
- `n_seeds: 1` — and the file is `sequences_0.txt`. The `_0` suggests we could provide
  multiple seeds (`sequences_1.txt`, ...). Not pursuing now — focus on single-seed signal first.
- Random gets +0.36 on condition_c. The condition_c metric appears tolerant of randomness
  — possibly a diversity/coverage measure. The condition_a/b metric appears not to reward
  uniform random.

## What this tells us
- The score being > 0 for random suggests "r" isn't pure correlation with a fixed target
  (which would give ~0). More likely it's a multi-component metric, or a diversity proxy.
- To beat random, I likely need to either (i) shift the per-string composition to a
  "good" region, or (ii) increase across-library diversity in some specific axis.
