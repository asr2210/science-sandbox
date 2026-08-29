# 007 — Dirichlet(0.3) + light motif insertion (0123 -> ACGT)

## Setup
Dirichlet(0.3) per-seq base + 0-5 motif insertions per sequence using
0->A, 1->C, 2->G, 3->T mapping.

## Result
- eval_01 mean=0.1354 (k562=0.0384, hepg2=0.1665, sknsh=0.2012)
- ≈ pure Dirichlet 003 (0.1349). Motifs added essentially nothing.

## Interpretation
With mapping 0->A,1->C,2->G,3->T, motif insertion is neutral on top of
compositional variance. Possible reasons:
1. Mapping is wrong
2. The motifs aren't strong enough (sparse insertion in 200bp)
3. The model isn't motif-sensitive in the way I expect
Next: try a different mapping with the same recipe.
