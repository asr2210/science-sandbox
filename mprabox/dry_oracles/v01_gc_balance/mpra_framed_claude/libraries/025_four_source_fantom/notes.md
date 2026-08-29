# 025_four_source_fantom

## Setup
4-source mega-pool: 12.5k cCRE + 12.5k ChIP + 12.5k Malinois + 12.5k
FANTOM5 CAGE peaks. CAGE peaks (FANTOM5 phase1+2 hg38, 209k entries)
mark TSSs of both genes and enhancer RNAs — mechanistically different
from the other three sources.

## Result — best eval_04 to date, eval_01 tied
- eval_01 = 0.6928 (**tied best**)
- **eval_04 = 0.6197 (best so far, vs prior best 0.6027)**
- eval_07 = 0.7453 (down from 0.7557 best)
- eval_08 = 0.1252 (~tied)
- eval_10 = 0.6577 (down from 0.6671)
- eval_13 = 0.7334 (down from 0.7472)

## Interpretation
Adding FANTOM5 CAGE peaks (vs cCRE/ChIP/Malinois 3-source):
- eval_01 saturates at the same 0.6928 ceiling
- eval_04 lifts +0.02 — best yet — because CAGE peaks encode
  transcription-output information that the other 3 sources lack
- eval_07/10/13 regress slightly (small budget for each source means
  less of the K562/HepG2/SKNSH-specific ChIP signal that those evals
  reward)

## Theory update → T16
Different evals weight different regulatory information types:
- eval_01: general activity → saturates at 0.6928 regardless of mix
- eval_04: cross-CT specificity → boosted by CT-specific Malinois
  AND by CAGE transcription evidence
- eval_07/10/13: TF-binding-dependent → favor ChIP-seq heavy mixes

For pure eval_01: 3-source mega-pool is best (0.6928).
For balanced multi-eval: 4-source mega-pool with FANTOM5 is best
(0.6928 eval_01 with eval_04 +0.02).

## Takeaway
FANTOM5 is a real addition (unlike DHS in exp 021). The 4-source mix
matches eval_01 best and exceeds on eval_04. Strong candidate for
final library if mean_r is the secondary criterion.
