# 021_four_source_mega

## Setup
13k cCRE + 13k ChIP + 12k Malinois + 12k DHS. Adds DHS as a 4th source
on top of the 3-source mega-pool to test if more diversity helps.

## Result — slight regression
- eval_01 = 0.6911 vs 3-source mega 0.6928 (−0.0017)
- eval_04 = 0.5920 vs 0.6004 (−0.008)
- Other evals tied or slightly worse

## Interpretation
DHS dilutes rather than helps. This is consistent with exp 008
(cCRE+DHS mix at 0.6835) and exp 007 (DHS alone at 0.6631) — DHS is
slightly weaker than cCRE/ChIP, and adding it reduces the per-sequence
training signal.

## Theory update → T12
3 sources (cCRE+ChIP+Malinois) is the sweet spot for diversity. A
4th source (DHS) is redundant with cCRE coverage and dilutes signal.

## Takeaway
3-source mega-pool (0.6928, exps 018 & 020) remains best. Won't add
DHS. Will explore other refinements: high-confidence ChIP-seq peaks
(top by score), different cCRE class weights, motif-density-filtered
sequences.
