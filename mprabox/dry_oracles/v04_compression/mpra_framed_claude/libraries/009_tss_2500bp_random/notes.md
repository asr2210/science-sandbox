# 009_tss_2500bp_random

50k random 200bp windows within ±2.5kb of any RefSeq TSS (promoter
zone). Tighter than 008 (±25kb).

## Result
eval_01: 0.5031 (vs 008: 0.5035; -0.0004)
mean across 14: 0.526 (vs 008: 0.525)

## Per-eval delta vs 008 (±25kb)
- eval_01: -0.000 (saturated)
- eval_03: +0.006
- eval_04: +0.007  (promoter zone matches eval_04 best)
- eval_06: +0.002
- eval_07: -0.010  (broad coverage preferred)
- eval_08: -0.001
- eval_10: +0.004
- eval_13: -0.002

## Interpretation
TSS focus has saturated. Going from ±25kb to ±2.5kb essentially holds
eval_01 at 0.503, with small per-eval shifts (evals 03/04/06/10
slightly prefer tighter focus; evals 07/13 prefer broader).

Importantly, ±2.5kb did NOT crater like cCREs (0.39). So tight TSS
isn't over-curating in the same way. Difference: cCREs are explicitly
chromatin-accessible elements (1-2% of genome), while TSS ±2.5kb is
~7% of genome and includes both active and inactive promoters across
all genes.

## Implication
The TSS lever is maxed out around +0.007 vs broad genomic. Need a
different axis to push eval_01 further. Candidates:
- Conserved regions (PhastCons)
- Multi-species sequences (mouse)
- DHS/ATAC-seq peaks (broader than cCREs)
- CpG island regions
- Mixture of multiple "active" sources
