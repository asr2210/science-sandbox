# 006 — Motif insertion on uniform random background

## Hypothesis
Inserting strong TF binding sites (3 per seq) covering K562/HepG2/SK-N-SH and
universal motifs should bias the per-seq predicted activity in a way that
correlates with labels for some cell lines.

## Setup
Background: uniform random 25%. Per seq: 3 distinct motifs from a 16-motif
basket (GATA1, KLF1, NFE2, HNF4, HNF1, C/EBP, REST, E-box variants, TATA,
CCAAT, Sp1, CREB, AP-1, NF-kB, MYC). Greedy non-overlapping placement.
Resulting base composition ~25% each.

## Result
- eval_01 mean=**0.8173** (K562 **0.8516**, HepG2 **0.7495**, SKNSH 0.8509)
- K562 +0.021 vs random
- HepG2 -0.129 vs random (big drop)
- SK-N-SH +0.013 vs random

## Interpretation
Motifs help K562 and SK-N-SH slightly, hurt HepG2 strongly. The fixed motif
set is not HepG2-aligned. Likely HepG2's predictor expects more
random/unbiased sequences (its scoring head may be very strong on background
sequences). Net: another worse-than-random result.

## Next
- 007: hybrid 25k strict + 25k random. Mechanical test for whether mixing
  designs averages or compounds.
