# 029 — IC-weighted TF sampling

## Setup
17 TFs / 3 motifs / PWM. Sample TFs softmax-weighted by per-TF information
content (T=4). High-IC TFs (USF2 IC≈19, JUN, SP1) get oversampled vs
low-IC ones (GATA1 IC≈10).

## Results
eval_01 = 0.3556. Within 010's noise band but on the HIGH side. eval_07
= 0.4069, eval_10 = 0.4324, eval_13 = 0.4203 — strong across the board.

## Insight
IC weighting is a mild positive signal — biasing toward sharper motifs
helps slightly. Best of the 028-030 attempts.
