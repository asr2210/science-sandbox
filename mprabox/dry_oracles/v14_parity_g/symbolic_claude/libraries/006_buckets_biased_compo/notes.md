# 006 4 buckets biased composition (HEAVY=0.85)

FIRST SIGNAL FOUND. eval_01 mean=0.0022 (up from -0.0011).
Driven by cond_b which is +0.0118 (vs ~0 before).
Most evals show similar pattern (b ≈ +0.01 across (01,14)/(02,05)/(03,12)/(06,11)).

Side effects:
- cond_a slightly negative on most evals
- cond_c slightly negative on most evals
- eval_07 a=0.0135 (preserved), eval_13 mean=-0.0070 (worse)

Hypothesis: cond_b rewards per-sequence compositional spread. Push harder.

Next: HEAVY=0.95, same 4-bucket design.
