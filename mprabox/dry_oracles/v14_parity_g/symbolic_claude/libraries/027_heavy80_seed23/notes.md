# 027 HEAVY=0.80 seed=23

eval_01 = -0.0022 (a=-0.0030, b=-0.0071, c=+0.0037). NEGATIVE.

Updates HEAVY=0.80 seed table:
- seed=42 → +0.0076 (b=+0.0105)
- seed=7  → +0.0030 (b=+0.0086)
- seed=23 → -0.0022 (b=-0.0071)  ← bad lottery

Avg of 3: +0.0028. cond_b NOT robust across seeds — went negative at seed=23.

Interesting: eval_13 = +0.0058 here (was +0.0050 at 023). cond_b on eval_13
is +0.0149, suggesting different eval sets respond to different seeds.

Implication: my "real signal" at HEAVY=0.80 is partly seed luck. Structural
signal is weaker than estimated. Strategy: more seed lottery or accept 023.
