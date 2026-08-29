# 022 — AT-rich scaffold (GC=20%)

## Setup
Same 17 TFs / 3 motifs / PWM, but scaffold base composition 40A/10C/10G/40T.

## Results
eval_01 = 0.1817. Catastrophic, matches 002 (GC=60% → 0.12).

## Insight
GC composition matters strongly. Uniform 25% GC is the sweet spot for the
predictor. Both AT-skewed and GC-skewed scaffolds collapse the score.
Notable: eval_07 stays high (0.39), eval_13 stays okay (0.31), suggesting
those evals are less sensitive to scaffold composition.
