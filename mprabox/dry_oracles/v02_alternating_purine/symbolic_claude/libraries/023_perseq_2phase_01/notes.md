# Exp 023 — per-seq 2-phase mix (phase 0/1)

## Result
eval_01 = 0.1479 (vs 0.1550 phase 0). Still worse, but better than
4-phase mix (0.1420). condition_c = 0.4109 preserved.

eval_07 → 0.1735 (huge lift from 0.1349). 2-phase mix specifically
benefits evals like eval_07 that want broader phase coverage.

## Interpretation
For eval_01: pure phase 0 is optimal (any phase dilution hurts a/b).
Cross-eval trade-offs are unavoidable given different evals' phase
preferences.

## Next
Try deterministic 4-pattern library (no noise, 12,500 rows of each
pure phase). Extreme structure test — does removing noise push
condition_c above 0.41 ceiling, or break it (NaN or variance loss)?
