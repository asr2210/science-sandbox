# Exp 008 — random per-position template, p=0.7

## Design
Each of 200 positions has a fixed *randomly chosen* preferred base
(seed=8). p=0.7 to follow template, 0.1 each for others.

## Result
eval_01 mean_r = **0.0977**, WORSE than baseline (0.1272) and far worse
than the period-4 0123 (Exp 006: 0.1550). condition_c ≈ 0.32 (lower
than baseline).

## Interpretation
Per-position bias by itself does NOT help. The lift in Exp 006 came
specifically from the **period-4 0123 ordering**. A random ordering
of preferred bases per position actively hurts the score.

The scorer rewards positional content aligned with a *specific*
periodic structure (likely 0,1,2,3,0,1,2,3,...). Random positional
biases collide with the scorer's expected pattern.

Note: eval_10 alone jumped to 0.1561 — one eval likes random structure.
Most others penalised it.

## Next
Test whether the specific 0123 ordering matters, or any period-4
permutation works equally:
- Exp 009: period-4 motif "0,2,1,3" at p=0.7. Same all-4-bases use,
  different ordering.
