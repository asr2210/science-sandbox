# 010 — Markov anti-staying (no adjacent repeats)

50k sequences where char[i] != char[i-1] always. Per-position marginal still uniform.

## Result
- eval_01: 0.1999 (drop of 0.19 from random's 0.394)
- All conditions dropped roughly proportionally.

## Interpretation
Forbidding adjacent same chars HURTS. Random uniform has P(adjacent same) = 0.25;
removing those repeats matches some structure that target rewards.

## Comprehensive theory
The target distribution appears to be roughly INDEPENDENT uniform per position
(i.e., random uniform itself):
- Per-position marginal uniform: ✓
- Per-sequence has Binomial(200, 0.25) compositions: ✓
- Positions are independent: ✓
- Adjacent chars uncorrelated: ✓

Any deviation in any of these axes HURTS. Random uniform may literally be
the optimum (or extremely close to it).

## Strategy revision
Stop trying to beat random. Use remaining budget to:
1. Confirm random reproducibility across seeds
2. Try a few "obviously safe" variations
3. Submit best uniform random library as final
