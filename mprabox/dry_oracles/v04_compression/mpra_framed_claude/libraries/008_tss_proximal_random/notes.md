# 008_tss_proximal_random

50k random 200bp windows from within ±25kb of any RefSeq TSS, across
all 22 autosomes. RefSeq from ncbiRefSeq.txt. 1.36Gb of TSS-flanked
territory (~45% of genome).

## Result
eval_01: 0.5035 — **new best** (vs 002: 0.4967, +0.007)
mean across 14 evals: 0.525 (vs 002: 0.524)

## Per-eval delta vs 002 (random genomic, 6 chroms)
- eval_01: +0.007
- eval_03: +0.003
- eval_04: +0.003
- eval_06: +0.004
- eval_07: +0.003
- eval_08: -0.005
- eval_10: -0.013
- eval_13: -0.015

Wins on the "main" evals (01, 03, 04, 06, 07), loses on the higher-
scoring evals (10, 13). Mixed picture; net positive on eval_01.

## Interpretation
TSS-proximal sampling provides a small bias that matches what the
test distribution wants for evals 01-07. Evals 10 and 13 prefer the
broader 6-chromosome sample.

This is the first library to break above 0.50 on eval_01.

## Implication
Transcriptional bias helps but only slightly. The 0.50 plateau is
real for natural-sequence libraries. To push further, I need either:
- An even tighter TSS focus (test next: ±2.5kb = promoter zone)
- A different axis (CpG islands, DHS, conserved regions, multi-species)
- Multi-source diversity within "active" sequence sources
