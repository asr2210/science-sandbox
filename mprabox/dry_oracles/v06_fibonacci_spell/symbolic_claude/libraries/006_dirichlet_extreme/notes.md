# 006 — Dirichlet(0.05) extreme compositions

## Setup
50K sequences. Per-seq composition from Dirichlet(0.05): very near
vertices (most sequences nearly constant in one nucleotide).

## Result
- eval_01 mean=0.1232 (k562=0.0352, hepg2=0.1500, sknsh=0.1845)
- WORSE than Dirichlet(0.3) = 0.1349

## Interpretation
Too-extreme composition saturates predictions (very biased sequences
all look similarly weak). Compositional sweet spot is moderate
(~Dirichlet(0.3)). Pure composition signal is near saturated at ~0.135.
