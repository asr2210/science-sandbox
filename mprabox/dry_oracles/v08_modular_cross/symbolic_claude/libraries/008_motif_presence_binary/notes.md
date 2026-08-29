# 008 motif_presence_binary

25,000 random uniform + 25,000 same with motif "01230123" inserted at center.
Tests binary motif sensitivity.

## Result
eval_01 = -0.0023 (worse).
**eval_08 = +0.0073 (highest single eval so far!)**
eval_04/09 = +0.0047 (positive).

## Eval_01 condition breakdown
- condition_a = -0.0076 (worse than random's -0.0003)
- condition_b = -0.0054 (worse than random's +0.0067)
- condition_c = +0.0060 (best so far! was -0.0025 random)

Motif insertion strongly hurt conditions a and b but improved condition_c.

## Implication
Different conditions of eval_01 reward DIFFERENT features:
- a: rewards 4-mer repeats (only +0.002, but never higher)
- b: rewards random uniform diversity
- c: rewards motif presence

Mean is constrained by lowest condition. Hard to maximize all three.

## Best eval_01 single-strategy so far
- 005 dirichlet: +0.0030
- 001 random: +0.0013
- All other experiments worse or comparable.
