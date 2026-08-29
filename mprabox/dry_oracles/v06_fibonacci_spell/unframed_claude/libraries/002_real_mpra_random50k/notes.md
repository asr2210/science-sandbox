# 002 — Real MPRA sequences (random 50k from Gosai dataset)

## What
50,000 randomly-sampled 200bp sequences from the Gosai et al. 2023 lentiMPRA dataset
(776k total sequences in K562/HepG2/SKNSH).

## Result
- eval_01 mean_r = 0.1439 (vs 0.1165 random; +0.027)
- k562_r ~0.054 (vs 0.004; **13x improvement**)
- hepg2_r ~0.174 (vs 0.154; small)
- sknsh_r ~0.203 (vs 0.192; small)
- Time: 13s (faster than random's 23s)

## Theory update
Real MPRA sequences boost K562 most strongly. The scorer rewards biological
realism, especially for K562. Modest absolute gain (+0.03) suggests the
scoring isn't pure "library as training data" — that would yield a much
larger gain. Possibly: oracle predicts activity per sequence, and metric is
correlation with some target. K562 may be hardest to learn from random.
