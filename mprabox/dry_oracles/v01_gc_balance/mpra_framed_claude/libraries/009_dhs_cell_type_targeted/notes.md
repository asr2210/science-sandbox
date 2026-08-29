# 009_dhs_cell_type_targeted

## Setup
50k DHS sites from 4 cell-type-relevant pools (12.5k each):
- K562: Myeloid/erythroid + Lymphoid
- HepG2: Cancer/epithelial + Digestive
- SKNSH: Neural
- INV: Tissue invariant

## Result
- eval_01 = 0.6638 (cf. exp 002 = 0.6921, exp 007 = 0.6631)
- eval_07 = 0.7501, eval_13 = 0.7345
- eval_04 = 0.5172
- eval_08 = 0.1195

## Interpretation
Targeting DHS to cell-type-matched components didn't help vs the
16-component stratified DHS (0.6631 → 0.6638, basically the same).
Both DHS variants under-perform cCREs (0.6921) by ~0.03 on eval_01.

This is informative: even when DHS is matched to the eval cell types, it
doesn't beat cCREs. The cCRE-DHS gap is therefore not about cell-type
distribution. It must be about *element quality / annotation criteria*:
cCREs include CTCF binding, H3K4me3 marks, and TF-bound classes that
DHS lacks, and these structural / epigenetic constraints select for
higher-quality regulatory elements.

## Theory update
"Match the eval cell type distribution" is one knob; "use the right
regulatory annotation" is another, and the latter matters more here.
cCREs remain the strongest base. Future experiments should *augment*
cCREs with complementary data (ChIP-seq peaks, ABC enhancer predictions)
rather than replace them with raw DNase / DHS data.
