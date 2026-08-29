# Exp 015 — 30K random hg38 + 20K cCRE (40% cCRE)

## Design
Push cCRE fraction from 20% (013) to 40%. GC=0.439; CpG=0.0135.

## Result
**eval_01 = 0.0470.** Tied/slightly below 013 (0.0493). Mean = 0.0439.
HepG2 = 0.0512.

## cCRE fraction sweep
| exp | cCRE % | eval_01 | HepG2 |
|-----|--------|---------|-------|
| 010 | 0% | 0.0480 | 0.0526 |
| 013 | 20% | 0.0493 | 0.0535 |
| 015 | 40% | 0.0470 | 0.0512 |
| 008 | 100% (PLS+pELS) | 0.0387 | 0.0391 |

## Interpretation
Sweet spot is near 20% cCRE; pushing higher costs eval_01 and HepG2 alike.
GC drift (0.41 → 0.44 → 0.60) tracks the regression — composition skew
hurts again once it gets above genomic mean by ~0.02. eval_08 spikes to
0.0501 (cCRE has distributional signature).

## Theory update
- cCRE-enrichment plateau confirmed. The lift from 0% → 20% is at noise
  (~0.001 on HepG2), and 40% reverts.
- The 0.05 eval_01 ceiling on natural-DNA libraries is REAL.

## Next step
Try the inverse: random hg38 EXCLUDING any cCRE-overlapping windows
(gene-desert-like). Tests whether NOT having cCREs hurts, ties, or
(unexpectedly) helps. If gene-desert ties 010, then regulatory content is
neither necessary nor sufficient for the eval_01 plateau.

## Time
43s wall, 12s evaluator.
