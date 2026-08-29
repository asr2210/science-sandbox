# Exp 015 — period-2 (0,2) template at p=0.7

## Result
eval_01 mean_r = 0.1007 — worse than baseline (0.1272) and far worse
than period-4 (0,1,2,3) at 0.1550. condition_c ≈ 0.29.

## Interpretation
Period-2 with only two preferred bases (0 and 2 alternating) is worse
than period-4 with all four bases cycled. The scorer specifically
rewards the period-4 four-base monotonic cycle, not period-2.

## Next
Test a period-16 template that contains ALL FOUR phases of (0,1,2,3)
within one cycle. The intuition: per-eval phase preferences differ;
a multi-phase template might lift more evals simultaneously without
sacrificing the primary metric.
