# 027 — 012 recipe with 400bp PLS context window

eval_01 = **0.4241** (within seed noise of 012's 0.4248). K562 0.591, HepG2 0.618, SK-N-SH 0.063.

Expanded the PLS context window from 200bp to 400bp around midpoint, letting fragments sample from more diverse offsets per PLS. Result is statistically indistinguishable from 012. Wider window doesn't add value: most informative offsets are within ±100bp of midpoint anyway.
