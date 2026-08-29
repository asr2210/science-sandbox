# 012 — 25k strict + 25k (random + 1 SKNSH motif each)

## Hypothesis
Replacing the random half of 007 with random + 1 SK-N-SH-specific motif
should lift SK-N-SH with minimal HepG2 cost (motif dose is 1 per seq, ~10
bp out of 200 bp = 5% perturbation per seq, vs 15% in 006).

## Setup
Motif basket: TTCAGCACCATGGACAG (REST/NRSE), CACCTG (E-box NEUROG),
CAGCTG (E-box ASCL1). Insert one motif per random-half sequence at a
random position.

## Result
- eval_01 mean=**0.8791** (vs 007 0.8780, +0.001)
- K562 0.852 (vs 0.862, -0.010)
- HepG2 0.907 (vs 0.911, -0.004)
- SKNSH 0.878 (vs 0.862, **+0.016**)

## Interpretation
SK-N-SH-specific motif insertion at low dose (1 motif per random half seq,
so motif density ~2.5% of total library bases) gives a clear +0.016 SK-N-SH
lift while costing only -0.010 K562 and -0.004 HepG2. Net positive but tiny.

This is encouraging — motif-targeted lift works at small doses. Suggests
that diluted, cell-line-specific motif augmentation can selectively lift a
weak cell line.

## Next
- 013: 2 SK-N-SH motifs per random half — does dose amplify lift?
- 014: 1 K562 motif per random half — can we lift K562 similarly?
- 015: combined 1 K562 + 1 SKNSH per random half.
