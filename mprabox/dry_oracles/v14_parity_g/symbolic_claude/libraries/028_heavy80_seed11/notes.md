# 028 HEAVY=0.80 seed=11

eval_01 = +0.0006 (a=-0.0043, b=+0.0085, c=-0.0024). Slightly positive.

Updated 4-seed table at HEAVY=0.80:
- seed=42 → +0.0076 (b=+0.0105)
- seed=7  → +0.0030 (b=+0.0086)
- seed=11 → +0.0006 (b=+0.0085)
- seed=23 → -0.0022 (b=-0.0071)

Mean across 4 seeds: +0.0023. cond_b averages ~+0.005.

cond_b is positive 3/4 times (only seed=23 had it negative). So cond_b
is sort-of robust but with one bad outlier draw.

eval_07 jumped to +0.0067 here (c=+0.0189). seed=11 lucky on eval_07 but
not on eval_01. Different evals reward different seed quirks.

Conclusion: 023 at +0.0076 is partly seed lottery. The expected signal at
HEAVY=0.80 is closer to +0.002-0.003. Try variance reduction next.
