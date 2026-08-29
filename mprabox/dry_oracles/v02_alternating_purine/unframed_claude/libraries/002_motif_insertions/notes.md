# 002 motif_insertions

50,000 sequences, each with 6 strong TF motifs (SP1, NFY, GATA1, HNF4A,
NEUROD, NRSF, AP-1, CREB, TATA, etc.) inserted at random positions in
random background.

## Results
- eval_01: mean=0.1265 (vs 0.1342 baseline) — slightly **worse**
- K562/HepG2 still ~0.01 (no change)
- SKNSH dropped from 0.3817 to 0.3598

## Interpretation
Motif insertion did **not** raise the signal. Best guess: the scorer rewards
library diversity / coverage, not motif content. Motifs reduce per-position
randomness, lowering effective diversity in some feature space the scorer cares
about. K562/HepG2 stuck at zero suggests the K562 signal is NOT motif-content
driven (in any naïve sense).

This rules out the "model trained on library, motifs win" hypothesis.
