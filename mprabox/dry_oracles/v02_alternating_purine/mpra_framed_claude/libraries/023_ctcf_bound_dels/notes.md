# Experiment 023 — CTCF-bound dELS subclass boost (FAILED)

## Design
- 8K dELS,CTCF-bound + 7K uniform + 5K CTCF-only + 5K DNH3 = 25K positives
- 25K paired far flanks

## Result — mean_r 0.140 (much worse than 013's 0.166)
- eval_06/11 = 0.144 (CRASH from 013's 0.218 — worst since random baseline)
- eval_10 = 0.146
- eval_13 = 0.148 (lift over 013's 0.126)
- eval_07 = 0.150

## Interpretation
Boosting a positive subclass at the cost of reducing uniform cCRE
breadth was catastrophic for eval_06/11. The K562 enhancer signal
requires diverse positive types (PLS, pELS, dELS, etc.), not depth in
one sub-class.

- 7K uniform (down from 13's 15K) → too few PLS/pELS/non-CTCF-bound dELS
- 8K dELS_CTCF + 5K CTCF-only = 13K CTCF-flavored positives (over-representation)
- The model likely overfit CTCF-specific patterns at the expense of
  general enhancer discrimination

## Next
024 = revisit eval_07 (013=0.177, 018=0.203). Try diversified positives
with broader uniform sampling — maybe 20K uniform + 5K CTCF + 5K DNH3
(scale up uniform from 013's 15K).
