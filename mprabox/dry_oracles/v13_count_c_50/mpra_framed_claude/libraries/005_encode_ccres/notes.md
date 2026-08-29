# Experiment 005 — ENCODE cCREs (curated regulatory enrichment)

## Design
50,000 ENCODE V3 cCREs sampled from chr8/19/21/22/X. Each centered on
cCRE midpoint, extracted 200bp window. Type mix: 35k dELS, 9.5k pELS,
2.4k PLS, 1.7k CTCF-only, 1.4k DNase-H3K4me3.

## Results vs prior best (multi-chrom genomic)
| eval | multi-chrom (004) | cCRE (005) | Δ |
|------|-------------------|------------|---|
| 01 ★ | **0.5553** | 0.4579 | **-0.10** |
| 04 | 0.5086 | 0.5790 | +0.07 |
| 07 | **0.6284** | 0.3353 | **-0.29** |
| 08 | 0.0208 | 0.4159 | **+0.40** |
| 13 | **0.6135** | 0.3158 | **-0.30** |

eval_07 and eval_13 dropped catastrophically. eval_08 recovered.
**Net: cCREs are WORSE than random genomic on the primary metric.**

## Why this is the most important result so far
My intuition said "regulatory enrichment → motif density → better model."
Wrong. The opposite: cCREs are a *narrower* slice of the genome, biased
toward GC-rich, motif-rich, often-active sequences. A model trained on
this narrower distribution:
- Becomes overconfident on enhancer-like inputs
- Fails to generalize to less-active sequences in the eval sets
- Loses calibration across the full activity range

This matches the recent literature (Genome Biology 2024, EpiBERT paper):
"the accuracy of genomic deep learning models is reduced in cell type-
specific accessible regions" — models overfit to the most-active regions
when trained on curated sets.

## Theory update
v4 → v5:
- "More motif density per sequence" is NOT the right axis to optimize.
- The library must span the *evaluation distribution* — including inactive,
  marginally active, and highly active sequences.
- Random genomic sequences automatically include this range (most genomic
  DNA is silent / low-activity). cCREs are conditioned on being active,
  which truncates the distribution.
- Generalization comes from teaching the model the *gradient* of activity
  across the full input space, not from showing it many high-activity
  examples.

## Implication: stop curating, start covering
- Best approach probably stays as diverse natural genomic (multi-chrom).
- Don't enrich for regulatory function.
- Possibly: add complementary axes (e.g., synthetic motif tests) BUT only
  if they cover gaps the natural distribution doesn't, not if they
  concentrate on the already-rich regions.
