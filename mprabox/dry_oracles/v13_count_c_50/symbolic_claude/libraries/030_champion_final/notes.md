# 030 champion_final — FINAL SUBMISSION

## eval_01 = 0.4152 (NEW BEST across all 30 experiments)

Recipe:
- Endpoints ~ Dirichlet(0.5)
- Linear gradient between endpoints (smooth positional composition)
- Markov rows ~ Dirichlet(0.25)
- Mix weight: 0.2 * Markov + 0.8 * gradient base

Per-condition:
- condition_a = 0.4547
- condition_b = 0.3672
- condition_c = 0.4235

All evals:
- eval_01 = 0.4152
- eval_02 = 0.4150
- eval_03 = 0.4106
- eval_04 = 0.4165
- eval_05 = 0.4150
- eval_06 = 0.4160
- eval_07 = 0.4307
- eval_08 = 0.2723 (anti-correlated metric — accepted loss)
- eval_09 = 0.4165
- eval_10 = 0.4112
- eval_11 = 0.4160
- eval_12 = 0.4106
- eval_13 = 0.4193
- eval_14 = 0.4152
