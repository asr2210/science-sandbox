# 018 — Homotypic clusters (3 motifs same TF)

## Setup
Same 17 TFs / 3 motifs/seq, but each sequence draws all 3 from ONE TF.

## Results
eval_01 = 0.3478 (vs 010 = 0.3644). Worse.

## Insight
Heterotypic mix > homotypic stacking on eval_01. The predictor doesn't reward
TF-stacking signal in the way real enhancers might. eval_07 actually drops
0.027, eval_13 essentially flat.

## Next
Try sharpened PWMs (more canonical motifs).
