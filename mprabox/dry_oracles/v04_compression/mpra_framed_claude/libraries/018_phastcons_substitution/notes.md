# 018_phastcons_substitution — notes

## Design
20K natural + 15K phastCons elements (LOD≥50, 100-way) + 10K DHS + 5K mouse.
Replaces cCRE with phastCons (conservation criterion instead of chromatin).

## Result
- eval_01 = 0.4926 (vs exp 011 = 0.5012, Δ = -0.0086, ~2σ below)
- eval_07 = 0.5941 (slight uptick over 011's 0.5946? no, 0.5946 → 0.5941, ~flat)
- eval_08 = 0.1014 (slight uptick)
- Time: 30s

## Interpretation
PhastCons substitution slightly hurts. Likely cause: phastCons elements
include many EXONIC/CDS regions (protein-coding is the most conserved),
which are not regulatory sequences and probably aren't well-represented
in the eval distribution.

Conservation as a SELECTION CRITERION mixes coding and non-coding
functional sequences. cCRE filters to noncoding regulatory specifically,
so it's a cleaner match for MPRA-style activity prediction.

## Implication
Selection criterion matters as much as source. The model needs noncoding
regulatory examples, not all-functional examples. Conservation alone
doesn't filter to the right subset.

To use conservation usefully I'd need to intersect phastCons WITH cCRE
(conserved AND regulatory), but that's nearly identical to cCRE alone
since most cCRE elements are at least moderately conserved.

## Lesson
The plateau is structural for "noncoding regulatory regions". Different
detection modalities (cCRE, DHS, ChIP, FANTOM) all converge here.
Conservation introduces new noise (coding sequences) without new signal.

## Next test
GC-stratified natural sampling. Sample 20K natural uniformly across GC
bins (instead of the bimodal natural GC distribution). Hypothesis: model
sees broader GC range, generalizes better to GC-extreme regulatory
regions that random sampling under-represents.
