# 009 — Exact 25%/25%/25%/25% per sequence

## Hypothesis
Removing the natural Binomial(200, 0.5) per-sequence composition variance
might either help (tighter prediction distribution) or hurt (out-of-training).

## Results
eval_01 = 0.3049 (random 0.3157). Drop ~0.01 — just past the noise floor.

## Implication
Even removing the natural composition variance HURTS slightly. The metric
prefers the FULL noisy realization of i.i.d. uniform random, including its
Binomial(200, 0.5) composition fluctuation.

## Next
Try real human regulatory sequences via webfetch.
