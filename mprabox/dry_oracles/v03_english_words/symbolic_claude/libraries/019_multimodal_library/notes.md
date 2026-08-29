# 019 — multimodal library composition

Mix of 5 sub-libraries (sizes 5k,5k,30k,5k,5k) with p_0 = 0.20,0.25,0.30,0.35,0.40.
Library mean p_0 = 0.30 (same as exp 011).

## Result
- eval_01: mean_r = **0.3758** (vs 0.4272 for exp 011) — **-0.0514 (terrible)**
- a = 0.5160, b = 0.5413, c = 0.0700

c IS slightly higher (0.070 vs 0.057 for exp 011), but a, b dropped massively.

## Conclusion
Per-seq composition variance HURTS heavily. The eval prefers TIGHT iid library structure.
Multimodal libraries lose far more in a, b than they gain in c.

Library should be drawn from a SINGLE composition (no mixing).
