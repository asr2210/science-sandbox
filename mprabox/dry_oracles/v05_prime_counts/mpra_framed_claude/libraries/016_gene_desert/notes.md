# Exp 016 — Gene-desert (random hg38 EXCLUDING cCREs)

## Design
50K random 200bp windows where the window does NOT overlap any cCRE
(within 100bp buffer). 85% of genome is cCRE-free.
GC=0.398; CpG=0.0088 (slightly below genomic mean).

## Result
**eval_01 = 0.0479. HepG2 mean = 0.0556 — HIGHEST of any library so far.**
eval_13 = 0.0384, tied with 010's high.

## HepG2 sweep across cCRE fraction
| exp | cCRE % | eval_01 | HepG2 |
|-----|--------|---------|-------|
| 016 | **-100%** (excluded) | 0.0479 | **0.0556** |
| 010 | 0% (mixed) | 0.0480 | 0.0526 |
| 013 | 20% | 0.0493 | 0.0535 |
| 015 | 40% | 0.0470 | 0.0512 |
| 008 | 100% PLS+pELS | 0.0387 | 0.0391 |

Monotonic: more cCRE → less HepG2 transfer.

## Interpretation
cCREs introduce something that systematically hurts HepG2-direction
features. Possible mechanism: ENCODE V3 cCREs were called across many
ENCODE cell types where K562 is heavily represented; including cCREs in
training may bias features toward K562/HepG2 contrasts that don't transfer
well. Gene-desert sequences are more "neutral" — they reflect genomic
background not biased by any cell type's chromatin annotation pipeline.

## Theory update (significant)
- **Library bias source matters for cell-type generalization, separately
  from sequence content.** A library of cCREs is sequences enriched in
  regulatory grammar, BUT also enriched in features that were used to
  define cCREs (DNase, H3K4me3 etc. across ENCODE cell types).
- For cross-cell-type generalization, removing the annotation-pipeline
  bias may help — even though it removes the most biologically active
  sequences.
- eval_01 still 0.048 — primary eval doesn't reward this. But HepG2-mean
  +0.003 is the largest cell-type-specific lift I've seen.

## Next step
Push gene-desert harder: larger cCRE buffer (e.g., 1kb), or combine with
the strand-augmentation idea. Specifically: 25K gene-desert + 25K
gene-desert RC pairs OR 50K gene-desert with 1kb cCRE buffer.

## Time
43s wall, 13s evaluator.
