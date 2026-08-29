# 015 — iid heavy bias toward '0'

p = (0.40, 0.20, 0.20, 0.20). 10pp boost (vs 5pp in exp 011).

## Result
- eval_01: mean_r = **0.4010** (vs 0.4272 in exp 011, 0.4200 baseline)
- a = 0.5581, b = 0.5825, c = 0.0625

## Conclusion
Pushing further HURTS. Linear extrapolation fails. Optimum is near 0.30 for '0'.

The function is concave with peak near p_0 ≈ 0.27-0.30.
