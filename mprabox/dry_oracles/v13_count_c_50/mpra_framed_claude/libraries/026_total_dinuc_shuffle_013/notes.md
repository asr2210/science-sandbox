# Experiment 026 — total dinucleotide shuffle of library 013

## Design
Take every sequence in library 013 (35k mc5 + 15k type-balanced cCRE)
and dinucleotide-shuffle it. Preserves per-sequence GC and dinuc counts
across the entire library; destroys all motif structure everywhere.

## Result vs 013 (unshuffled)
| eval | 013 | 026 (full shuffle) | Δ |
|------|-----|---------------------|---|
| 01 ★ | **0.5765** | 0.4663 | **-0.110** |
| 04 | 0.5774 | 0.4109 | -0.166 |
| 07 | 0.6037 | 0.5159 | -0.088 |
| 08 | 0.1730 | **0.1984** | +0.025 |
| 10 | 0.5087 | 0.4755 | -0.033 |
| 13 | 0.5865 | 0.5016 | -0.085 |

## Conclusive decomposition of eval_01 = 0.5765
| component | contribution |
|-----------|--------------|
| floor (uniform random, exp 001) | 0.129 |
| dinuc composition of library (026 - floor) | +0.337 |
| motif grammar in mc5 BASE (013 - 026, esp. base part) | +0.110 |
| cCRE supplement composition (017 - 004 base) | +0.022 |
| **Total** | **0.576** |

## What the model learns
The model learns TWO distinct signals:
1. **Composition / k-mer statistics** (0.337 contribution) — from the
   library's average composition. Captured by dinucleotide structure;
   transferable even with shuffled sequences.
2. **Motif grammar** (0.110 contribution) — from the BASE mc5 sequences'
   real motif structure. Shuffled the base, this drops away.

The cCRE supplement (+0.022) acts purely via composition shift; its
motif content does NOT contribute (per exp 017).

## Key asymmetry: BASE vs SUPPLEMENT
- BASE: motif structure matters (+0.110 from grammar)
- SUPPLEMENT: composition only (+0.022 from GC distribution)

So the base provides the REGULATORY GRAMMAR learning material;
the supplement provides COMPOSITIONAL TUNING toward the eval distribution.

## eval_08 is special
eval_08 gained +0.025 from FULL shuffle — it actually PREFERS pure
composition over motif structure. This eval rewards pure k-mer
prediction and is hurt by motif-grammar features (which add noise to
its pure composition signal).

## Implication
Cannot break the 0.5765 ceiling by removing motif structure (it's
needed in the base). Cannot break it by adding more motif content
to the supplement (it doesn't help). The remaining lever is to
provide MORE/BETTER motif content in the BASE, or to better tune
composition of the supplement.
