# 011 — iid mild bias toward '0'

p = (0.30, 0.2333, 0.2333, 0.2333). Each char iid with these probabilities.

## Result
- eval_01: mean_r = **0.4272** (vs 0.4200 baseline) — **+0.0072 IMPROVEMENT**
- a = 0.5965, b = 0.6279, c = 0.0571 (all UP from baseline)

## Breakthrough
This is the first experiment to BEAT iid uniform baseline!

Combined with 012, 013, 014 (biases toward '1', '2', '3'):
- '0' bias: +0.0072 (BEST)
- '1' bias: -0.0024
- '2' bias: -0.0042
- '3' bias: -0.0121 (WORST)

**The eval has a strong per-char preference: '0' > '1' ≈ '2' > '3'.**

## Status: 11/30 used
