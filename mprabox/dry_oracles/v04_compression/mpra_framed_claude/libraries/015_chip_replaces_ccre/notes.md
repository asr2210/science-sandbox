# 015_chip_replaces_ccre — notes

## Design
20K natural + 15K ReMap ChIP peaks + 10K DHS + 5K mouse.
A/B test against exp 011 (same structure, ChIP substitutes for cCRE).

## Result
- eval_01 = 0.5002 (vs exp 011 = 0.5012; vs exp 014 same-design = 0.4971)
- Within noise band (±0.004) — statistically indistinguishable from 011.
- eval_04 = 0.5206 vs 011's 0.5180 (+0.0026, also within noise)
- eval_08 = 0.1019 (small uptick, also within noise)
- Time: 25s

## Interpretation
**In-vivo TF binding (ChIP) is the same information as accessibility
(cCRE/DHS) at the model's level.** Replacing 15K cCRE with 15K random
ChIP-summit windows gives identical eval_01 within noise.

This is the THIRD source-substitution experiment showing the same thing
(011 with cCRE, 015 with ChIP, 013 added FANTOM5). The model has saturated
on "regions identified by some regulatory atlas" — modality of detection
(chromatin marks, DNase, CAGE, TF ChIP) doesn't matter.

## Implication
The plateau at ~0.50 is a regulatory-atlas plateau, not a chromatin-vs-
binding distinction. To exceed it I need a different KIND of sequence
content, not a different KIND of region annotation.

Candidates remaining:
- Augmentation (reverse complement) — doubles data via strand symmetry
- Curated within-class sampling (motif-dense windows, k-mer diverse)
- Conserved sequences (phastCons / phyloP) — different selection criterion
- Variant-perturbed natural (synthetic mutations on natural backbone)

## Next test
Reverse-complement augmentation. 25K mix (exp 011 ratios scaled to 25K)
plus 25K of their reverse complements. Tests whether explicit strand
symmetry in training data helps, independent of architecture.
