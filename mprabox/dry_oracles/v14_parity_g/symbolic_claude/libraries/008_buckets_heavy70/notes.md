# 008 4 buckets HEAVY=0.7

eval_01 mean=0.0023, b=0.0052, c=0.0020 (BOTH positive now!).
All 14 evals positive or near zero. Best so far for global picture.

eval_03/12: 0.0066, eval_08: 0.0068, eval_13: 0.0051.

cond_b vs HEAVY for eval_01:
- HEAVY=0.7: b=0.0052
- HEAVY=0.85: b=0.0118 (peak so far)
- HEAVY=0.95: b=0.0005

cond_c vs HEAVY for eval_01:
- random (0.25): c=-0.0053
- HEAVY=0.7: c=+0.0020 (peak so far)
- HEAVY=0.85: c=-0.0028
- HEAVY=0.95: c=-0.0018

cond_b prefers HIGH bias (~0.85); cond_c prefers MODERATE bias (~0.7). Conflict.
For eval_01 the sum balances similarly.

Next: HEAVY=0.5 to check if c keeps growing with less bias.
