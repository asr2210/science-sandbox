# Experiment 022 — 32-pool + per-base mutation (PWM-style noise)

## Result
eval_01 = 0.3412 (seed=53, p_mut=0.15). Worse than 32-pool seed=53 (0.369).

## Interpretation
Mutating motif bases at p=0.15 weakens motif identity. The scorer apparently
keys on canonical motif strings; corrupted versions don't help. Confirms
that **clean** canonical motifs > stochastic motif sampling.
