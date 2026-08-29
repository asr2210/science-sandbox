# 018 — seed lottery on best setup

Same p as exp 011 (0.30, 0.2333, ...) but seed 1234567 instead of 42.

## Result
- eval_01: mean_r = **0.4222** (vs 0.4272 for exp 011)

## Conclusion
Seed lottery is HIGH NOISE.
- Uniform iid: seed 42→0.4200, seed 1234567→0.4239 (Δ=+0.0039)
- p=(0.30,...): seed 42→0.4272, seed 1234567→0.4222 (Δ=-0.0050)

True signal from '0' bias is closer to mean(0.4272, 0.4222) - mean(0.4200, 0.4239) = **+0.0027** (small).

Implication: noise floor is ~±0.005 per seed. Hard to distinguish signals below that.
