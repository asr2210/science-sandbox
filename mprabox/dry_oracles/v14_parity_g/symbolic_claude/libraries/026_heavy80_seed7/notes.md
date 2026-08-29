# 026 HEAVY=0.80 seed=7 (verification of exp 023 peak)

eval_01 mean=+0.0030 (b=+0.0086, c=-0.0004, a=+0.0006).

Compare to exp 023 (HEAVY=0.80 seed=42): eval_01=+0.0076 (b=+0.0105, c=+0.0088).

Verdict: HEAVY=0.80 has a real positive signal across seeds.
- cond_b: 0.0105 (seed=42) vs 0.0086 (seed=7) → robust ~+0.009
- cond_c: 0.0088 (seed=42) vs -0.0004 (seed=7) → very noisy, partly seed luck
- cond_a: 0.0035 (seed=42) vs 0.0006 (seed=7) → marginal

The narrow peak at HEAVY=0.80 (vs 0.78/0.82 negative at seed=42) seems to be
partially a real structural effect, partially noise interaction. Avg(0.0076, 0.0030)
= +0.0053, which is still the best HEAVY value across seeds.

Implication: cond_b drives the signal robustly. cond_c rewards are seed-dependent
at HEAVY=0.80 and may need different structure entirely.
