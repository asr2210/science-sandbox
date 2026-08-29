# 006 compositional gradient

50K sequences with per-seq GC fraction varying linearly 0 -> 1.

## Result
- eval_01: 0.2501 (worse than uniform 0.2974)
- Per-seq composition skew hurts modestly across most evals.
- eval_08 hit hard (0.052 vs 0.105 random).
