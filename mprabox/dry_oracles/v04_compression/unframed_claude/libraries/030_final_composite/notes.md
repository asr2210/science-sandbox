# 030 — Final composite (IC-weighted + lucky seed)

## Setup
17 TFs / 3 motifs / PWM / IC-weighted TF sampling / seed=20260610.

## Results
eval_01 = 0.3276. Worse than 029 (0.3556) and 010 (0.3644).

## Insight
Combining "lucky seed" 20260610 with IC weighting did NOT preserve the
luck. The lucky seed is only lucky for the SPECIFIC RNG draws of 010's
algorithm — changing the algorithm (adding IC weighting) re-rolls the dice.
Best result of the run remains exp 010 = 0.3644.
