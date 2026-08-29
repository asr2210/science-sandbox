# 019_max_variance_mix

Mixed 5 real-DNA sources × 10k each to maximize per-sequence GC variance:
- chr22 random (gene-dense, ~48% GC)
- whole genome random (~41% GC)
- cCRE all categories (regulatory, ~50% GC)
- cCRE PLS+DNase-H3K4me3 (high GC, CpG-island-rich)
- chrX random (heterochromatin-leaning, AT-rich)

## Result
eval_01: **0.6895 — NEW BEST** (beats cCRE-all 0.6840)
eval_07: 0.7615 (new best, beats whole-genome 0.7595)
eval_13: 0.7549 (new best)
eval_04: 0.5818

## Interpretation: VARIANCE HYPOTHESIS CONFIRMED
Exp 018 collapsed when we restricted GC to 40-55%. This exp does the
opposite — explicitly span 30-65% GC across sources — and beats every
prior single-source library.

Score is bounded above by within-library *variance* in features the
scorer reads. Wider per-seq distribution → more signal to correlate
on → higher r.

PLS alone (exp 008) crashed at 0.09. But PLS as one of FIVE sources
contributes signal without dragging score down: composition extremes are
information when mixed with their opposites.

## Next
Try pushing variance further: add even more extreme sources
(chrY heterochromatin, telomere-adjacent regions, vs CpG island cores).
Test the bimodal hypothesis explicitly.
