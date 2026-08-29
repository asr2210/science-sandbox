# 008 random uniform (seed=1) — noise floor check

Same as exp 001 but with seed=1. Pure noise-floor check.

## Result
- mean_r = 0.8494 (eval_01 = 0.8587)
- vs seed=0: mean = 0.8516, eval_01 = 0.8620
- Difference 0.002–0.003

## Takeaway
Noise floor ~0.003. Any observed effect > ±0.01 between libraries is real.

## Skill update
Add to `skills/noise_floor.md`: random-uniform seed-to-seed noise is ~0.003
on mean_r and eval_01. Treat smaller differences as inconclusive.
