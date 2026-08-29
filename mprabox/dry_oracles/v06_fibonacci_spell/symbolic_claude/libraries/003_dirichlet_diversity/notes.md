# 003 — Dirichlet diversity

## Setup
50K sequences. Per-sequence composition drawn from Dirichlet(0.3, 0.3,
0.3, 0.3), sampled length-200.

## Result
- eval_01 mean=0.1349 (k562=0.0376, hepg2=0.1673, sknsh=0.1999)
- vs baseline 0.1183 (k562=0.0090): K562 ~4x improvement

## Interpretation
Compositional variance helps r. K562 in particular benefits the most
from non-uniform compositions. Suggests both eval and reference models
respond strongly to nucleotide composition (especially for K562).
