# Exp 001 — Uniform random baseline

## Design
50,000 sequences, length 200, each char iid uniform from {0,1,2,3}.
Seed=20260603.

## Result
mean_r per eval:
- eval_01: 0.4848 (a=0.5241, b=0.5009, c=0.4295) — PRIMARY
- eval_02: 0.4851 (a=0.5239, b=0.5012, c=0.4301)
- eval_03: 0.4843
- eval_04: 0.4440 (low)
- eval_05: 0.4851 (= eval_02 exactly)
- eval_06: 0.4830
- eval_07: 0.5200 (high)
- eval_08: 0.1613 (very low — different scale or harder eval)
- eval_09: 0.4440 (= eval_04 exactly — may be duplicate)
- eval_10: 0.4700 (condition_a spread 0.54 vs 0.39 — most spread)
- eval_11: 0.4830 (= eval_06)
- eval_12: 0.4843 (= eval_03)
- eval_13: 0.4992
- eval_14: 0.4848 (= eval_01)

## Observations
- "r" likely refers to correlation (Pearson?) → naming convention "mean_r".
  Or could be a normalized per-sequence score.
- Several eval pairs return identical numbers (01==14, 02==05, 03==12,
  04==09, 06==11). Likely 9 unique evals replicated.
- Condition c is consistently weakest. Condition a strongest.
- eval_08 stands out at 0.16 — possibly a different scale or hard eval.
- Total time 54.5s wallclock, 24.1s scoring time. Affordable budget.
