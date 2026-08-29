# 016 dirichlet_plus_motif

50k = 25k Dirichlet(0.5) + 25k Dirichlet(0.5) with '01230123' at center.

## Result
eval_01 = +0.0014 (worse than Dirichlet alone +0.0030). Big eval_03/eval_08 jumps via condition_c.

## Eval_01 conditions
| | a | b | c | mean |
|---|---|---|---|---|
| dirichlet alone | +0.0003 | +0.0070 | +0.0016 | +0.0030 |
| dirichlet+motif (this) | +0.0025 | -0.0018 | +0.0034 | +0.0014 |

Motif boosts c (+0.0016 → +0.0034) and a (+0.0003 → +0.0025) but tanks b (+0.0070 → -0.0018).
Net negative on eval_01.

## Other notable
- eval_03/12 c = +0.0136 (huge boost!)
- eval_08 c = +0.0138 (huge!)
- eval_13 a = +0.0142 (huge!)

These evals love Dirichlet+motif. For eval_01, pure Dirichlet still wins.
