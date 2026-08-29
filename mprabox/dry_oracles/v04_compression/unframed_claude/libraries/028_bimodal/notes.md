# 028 — Bimodal mixture (25k motif + 25k random)

## Setup
50% sequences exp-010-style PWM+3-motifs, 50% pure uniform random.

## Results
eval_01 = 0.3281. Worse than either pure config.

## Insight
Bimodal libraries don't help Spearman. Mixing low-mode (random ~0.32) with
high-mode (motif ~0.34) averages out. The eval rewards consistent strong
signal across all 50k, not a wider variance.
