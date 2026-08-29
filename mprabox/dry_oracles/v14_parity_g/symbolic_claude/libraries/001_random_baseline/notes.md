# 001 random uniform baseline (seed 42)

mean_r ≈ 0 across all 14 evals; near pure noise.
Duplicate evals same as v08/v10 pattern:
- (01,14), (02,05), (03,12), (04,09), (06,11) identical
- 07, 08, 10, 13 singletons

eval_03/eval_12 are tied for highest (0.0036, driven by a=0.0134).
eval_13 has the lowest (-0.0047, driven by a=-0.0111).

Per-condition decomp shows a, b, c all near 0. So this run requires
structural design to get a score. Random uniform is NOT the answer.

Took ~84s.
