# 019 — Sharpened PWMs (power=2)

## Setup
PWM raised to power 2 then renormalized. Pushes samples toward consensus.

## Results
eval_01 = 0.3489 (vs 010 = 0.3644). Worse.

## Insight
017 (more PWM variation per TF) was worse; 019 (less variation per TF) is
also worse. Natural PWM stochasticity is the sweet spot.
