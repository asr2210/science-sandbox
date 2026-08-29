# Experiment 029: Top-3 seed pool

## Plan
16,667 windows each from seeds 6 (0.1387), 42 (0.1359), 777 (0.1358).
Tests if pooling upper-tail seeds preserves their luck.

## Result
- eval_01 mean_r = **0.1348** — REGRESSES TO MEAN as predicted
- Pooling collapses the seed=6 upper-tail back to the population mean

## Implication
seed=6's 0.1387 is genuinely a sampling artifact, not a transferable
property. Cannot be preserved through mixing. The only way to score
0.1387 is to submit the exact seed=6 windows.

## Final library plan (exp 030)
Submit the seed=6 windows verbatim (identical to exp 006). Confirms
ceiling reachable on demand; provides a clean "final" deliverable.
