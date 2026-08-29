# Experiment 024 — GC + CpG joint-matched supplement

## Design
35k mc5 + 15k mc5 windows matching cCRE GC histogram, with top-CpG
selected within each GC bin. Supp GC 0.527 matches cCRE (0.527).
Supp CpG mean 9.72/200bp vs cCRE 6.33 — over-enriched.

## Result vs 013 and 022
| eval | 013 (cCRE) | 022 (GC-only) | 024 (GC+CpG) | 024-022 |
|------|------------|----------------|---------------|---------|
| 01 ★ | **0.5765** | 0.5731 | 0.5658 | -0.007 |
| 04 | 0.5774 | **0.5777** | 0.5629 | -0.015 |
| 07 | **0.6037** | 0.6003 | 0.5978 | -0.003 |
| 08 | 0.1730 | 0.1566 | 0.1612 | +0.005 |
| 13 | **0.5865** | 0.5843 | 0.5821 | -0.002 |
| mean8 | 0.5705 | 0.566 | 0.5604 | -0.006 |

## Verdict: forcing CpG enrichment HURTS
Top-CpG-within-bin selection produces a supplement that over-shifts
toward CpG islands. Library loses diversity in the supplement; mean8
drops, eval_01 drops 0.007 below 022 (GC-only matching).

## Theory refinement
The cCRE supplement's value is NOT about maxing out CpG density. cCRE
distribution includes NATURAL variation: some CpG-rich (PLS,
DNase-H3K4me3), some CpG-poor (dELS, CTCF-only). The model benefits
from this natural compositional VARIETY within high GC, not from
uniformly high CpG.

GC-histogram matching (022) preserves natural CpG variance via random
within-bin sampling. Top-CpG selection (024) destroys this variance
and over-fits to CpG islands.

## Refined theory v17
The cCRE supplement provides a NATURAL composition distribution that
the model can learn from. The naturalness — covering many compositional
sub-modes — matters more than any particular average. Engineering
single-axis maxima (top-CpG, narrow high-GC) damages the diversity.

**Lesson: random sampling within composition bins > top-K selection.**
022's random within-bin sampling preserves the natural variance that
the cCRE supplement provides.
