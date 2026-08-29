# Experiment 014 — 70/30 multi-chrom + PhastCons-centered

## Design
35k multi-chrom-5 + 15k 200bp windows centered on PhastCons elements
(≥30bp, 100-way vertebrate alignment) from chr8/19/21/22/X.

## Results vs cCRE-supplemented (009)
| eval | 009 (cCRE) | 014 (PhastCons) | Δ |
|------|------------|-----------------|---|
| 01 ★ | **0.5748** | 0.5541 | -0.021 |
| 04 | **0.5695** | 0.4957 | -0.074 |
| 07 | 0.6069 | **0.6353** | +0.028 |
| 08 | 0.1560 | -0.0032 | -0.159 |
| 13 | 0.5897 | **0.6186** | +0.029 |
| mean8 | 0.581 | 0.560 | -0.021 |

## Why PhastCons lost
GC content. PhastCons-centered windows have mean GC 0.424 vs cCRE windows
~0.50. The PhastCons supplement LOWERED the library GC and especially hurt
eval_08 (which collapses with low GC).

Interestingly, eval_07 and eval_13 *gained* — PhastCons adds genomic
diversity these evals reward.

## What this confirms
- The cCRE supplement's value is partly compositional (GC), partly
  functional (TF motif density).
- PhastCons provides the functional part (conservation = constraint =
  motifs) but not the GC part.
- Pure functional curation without GC enrichment hurts the
  composition-sensitive evals more than it helps the grammar evals.

## Next: combine sources
A multi-source mix (cCRE + PhastCons) might capture the diversity gain
from PhastCons (eval_07/13) without losing the GC gain from cCRE (eval_08).
