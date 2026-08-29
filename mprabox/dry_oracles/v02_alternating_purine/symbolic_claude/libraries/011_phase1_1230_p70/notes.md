# Exp 011 — phase-shifted period-4 (1,2,3,0) at p=0.7

## Result
eval_01 mean_r = **0.1181** (worse than phase-0 0.1550 but better than
wrong-permutation 0.0949). condition_c ≈ 0.41 (still high!), but
condition_a/b dropped to negative (-0.028 vs +0.027 for phase 0).

## Per-eval flips
- eval_01: 0.155 → 0.118 (phase 0 better)
- eval_07: 0.135 → 0.166 (phase 1 better!)
- eval_13: 0.114 → 0.157 (phase 1 better!)
- eval_06/11: 0.197 → 0.104 (phase 0 better)

Different evals prefer different phases.

## Interpretation
- The period-4 structure itself is what condition_c rewards (similar c
  ≈ 0.41 regardless of phase).
- Conditions a/b are PHASE-sensitive — they shift sign with phase.
- For eval_01 (primary metric), phase 0 = 0,1,2,3 is optimal.

## Next direction
Stay on phase 0 for eval_01. Test whether **ascending structure** is
the lever generally or specifically period-4. Try a "blocked ascending"
template: positions 0-49 prefer 0, 50-99 prefer 1, 100-149 prefer 2,
150-199 prefer 3. If this beats period-4, ascending arrangement is the
key signal. If worse, period-4 is specifically rewarded.
