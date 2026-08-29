# 015_malinois_cell_type_specific

## Setup
50k Malinois oligos selected as TOP by std([K562, HepG2, SKNSH] log2FC) —
the most cell-type-specific MPRA-measured sequences. Threshold: std ≥ 0.78
(out of natural range 0–~3).

## Result — mixed
- eval_01 = 0.6600 (cf. random Malinois 0.6856, cCRE 0.6921, **−0.03**)
- **eval_04 = 0.6300 vs cCRE 0.5977 (+0.03 win!)**
- eval_07 = 0.7061 vs 0.7562 (worse)
- eval_08 = 0.1259 (slightly improved over cCRE's 0.1248)
- eval_10 = 0.5982 vs 0.6673 (worse)

## Interpretation
First library that *meaningfully shifts* eval_04 above cCRE. eval_04
(and its duplicate eval_09) responded to cell-type-specific training data
by +0.03. So eval_04 measures something like cell-type-discrimination
that's enriched in CT-specific MPRA sequences.

Meanwhile eval_01, eval_07, eval_10 all dropped. The distribution mismatch
from picking only "specific" sequences hurts the bulk correlation. But the
fact that *one* eval moved suggests these evals score different
sub-properties of the model:
- eval_01/07/10: general activity prediction → favored by natural-
  distribution training data (cCRE, random Malinois)
- eval_04/09: cell-type-specific activity → favored by CT-specific
  training data

## Theory update → T7
Different evals reward different training distributions. A library
optimized for one may degrade others. To max eval_01 specifically:
keep cCRE base; do NOT bias toward CT-specific sequences.
But to max a *composite* score, mixing cCRE + small CT-specific subset
might be the best blend.

## Takeaway
Pure CT-specific selection is a net loss on eval_01. But the eval_04
boost suggests a combined library (cCRE majority + small Malinois CT-
specific minority) might beat cCRE alone slightly across the board.
Will test in a later experiment.
