# 018 grad_markov_hybrid

50/50 mix of Markov transition + position-dependent gradient composition.

## Result
- eval_01: 0.4010 (vs 0.4078 pure gradient)
- a: 0.4082 (DOWN from 0.4508)
- b: 0.3744 (UP from 0.3634)
- c: 0.4204 (UP from 0.4092)
- eval_04: 0.4351 (jumped from 0.4005 pure gradient!)
- eval_08: 0.3246 (jumped from 0.2504)

Markov mixing helps b and c (and other evals) but tanks a more than the rest gains.
Try lighter Markov weight (e.g., 20%) to keep a high while still helping b.
