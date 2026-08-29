# Exp 022 — period-4 (0,1,2,3) at p=0.4

## Result
eval_01 = 0.1534. condition_c = 0.4046.

## Interpretation
p-curve fully mapped: p=[0.4, 0.75] all give 0.153-0.155 (flat plateau).
p=0.9 drops to 0.131. p is not the lever.

## Next
Try 2-phase per-seq mix: each row picks phase ∈ {0, 1} (50/50).
Tests whether 2 phases (less canceling than 4) preserves a/b lift
better while diversifying. If eval_01 > 0.155 → break the ceiling.
If 0.14-0.15 → 4-phase Exp 020 result extends.
