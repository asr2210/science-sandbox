# Experiment 018 — 35k motifs (35-50/seq) + 15k pELS

## What I tested
Same as 012 but DOUBLED motif density (35-50 inserts per seq vs 15-25).

## Result — eval_07 RECORDS, eval_08 collapse
- **eval_07: mean=0.0109, K562=0.0087, HepG2=0.0045, SKNSH=0.0195**
  — NEW RECORDS on eval_07 mean (vs 009's 0.0088) and eval_07 SKNSH
  (vs 012's 0.0162).
- **eval_04/09: 0.0073** — record on these (vs 017's 0.0047)
- **eval_13: mean=0.0054, all 3 cells positive** — best balanced
  eval_13 ever
- eval_08: -0.0072 (LOST big — was 012's 0.0117)
- eval_10: 0.0003 (lost)
- Many evals slightly negative
- Mean across 14 ≈ 0.0008

## What this tells me
**Motif density is a major dimension.** Doubling density:
- HUGE wins on eval_07 (mean+SKNSH records), eval_04/09, eval_13 balanced.
- BIG loss on eval_08.

Different densities serve different evals. Sequences with many motifs
look more like "saturated regulatory elements" — model learns features
that benefit eval_07 but lose the simpler co-occurrence patterns
eval_08 needs.

## Updates to theory
**v3.10 → v3.11:** Motif density per sequence is an INDEPENDENT
optimization axis from motif vocabulary or library mixing. Different
densities create different "regulatory grammars" that the model
learns. The 14 evals are sensitive to different grammars.

This implies a powerful new strategy: MIX MOTIF DENSITIES within the
library. Have some seqs at 15-25 (eval_08-friendly) and others at
35-50 (eval_07-friendly). Since motif scaffolds occupy 35k slots,
splitting them 17.5k/17.5k may capture BOTH eval gains.

## Next
Test mixed-density library: 17.5k motifs @ 15-25 + 17.5k motifs @
35-50 + 15k pELS. If both density grammars survive at half-strength,
mean climbs above 012.
