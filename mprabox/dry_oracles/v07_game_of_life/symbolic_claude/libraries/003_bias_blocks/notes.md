# 003 — Compositional bias probe (70% biased blocks)

4 blocks of 12,500 sequences. Each block heavily biased (70%) toward one character.

## Results (vs baseline 0.3943)
- eval_01: 0.3296 (Δ = -0.065)
- eval_08: 0.2068 (Δ = -0.069)
- eval_13: 0.3578 (Δ = -0.048)
- All evals DROPPED.

## Interpretation
Heavy single-character bias (averaged across all 4 chars) reduces score. Two possibilities:
1. Bias hurts uniformly (all 4 patterns score ~equally low at 0.33)
2. Some chars help, others hurt strongly — but average still negative

Either way, **strong global compositional bias is suboptimal**. The function does not reward "more 0s" or "more 1s" as a class — it rewards something more structured.

## Theory update
- Function is likely position-specific (matching some target template per position)
- Random scores ~0.39 because uniform random has average overlap with target
- To improve, need to align sequences to a position-specific target, not skew composition globally

## Next test
Position-specific pattern: e.g., period-4 "0123" repeated. Test if matching a periodic template boosts scores.
