# Exp 020 — per-sequence random phase period-4

## Result
eval_01 = 0.1420 (vs 0.1550 phase 0). condition_c = 0.4106 (preserved!),
but a=b=0.0077 (collapsed from 0.0316).

eval_07 lifted to 0.1546 (vs 0.1349); eval_10 to 0.1541. Phase mixing
trades eval_01 for other evals.

## Interpretation
condition_c is phase-invariant (signal preserved at 0.41 regardless).
condition_a/b are phase-sensitive: each eval prefers a specific phase.
eval_01 prefers phase 0. Per-seq random phase = average across all
phases = ~0 for a/b on each individual eval.

## Next
Test positional gradient of template strength — first 100 positions
high p (0.95), last 100 positions lower p (0.5). If eval is positionally
weighted (e.g., later positions matter more), gradient direction matters.
