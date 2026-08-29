# 007_promoter_dense

## Design
50,000 = 10,000 PROMOTER-class cCREs × 5 random-offset 200bp tiles
each. Promoter-class = PLS + PLS,CTCF-bound + DNase-H3K4me3 +
DNase-H3K4me3,CTCF-bound (66,812 total). Promoters are the most
cell-type-invariant regulatory class.

## Hypothesis
Promoters are universally regulatory (R=0.78-0.95 across cell types
in literature). Focusing on them should be the most generalizable
library and may lift performance above mixed-cCRE-dense (0.318).

## Result vs 005
                eval_01  K562    HepG2   SKNSH   eval_08
005 cCRE dense: 0.3177   0.146   0.185   0.622   0.076
007 PLS dense:  0.3146   0.138   0.179   0.627   0.076

Slight DROP (-0.003). K562 -0.008, HepG2 -0.006, SKNSH +0.005.

## Interpretation
Promoter focus is NOT a strict improvement. Mixed cCRE (which
includes enhancers) is slightly better — probably because enhancer-
specific motifs in dELS/pELS regions contribute signal that pure
promoters can't.

Confirms plateau: no source-of-natural-regions choice within cCRE
classes lifts performance.

## Theory T5 (refined)
Mixed-class natural cCREs are roughly the best natural-source choice.
Plateau ~0.32. Need to test if mixing natural cCRE with NON-cCRE
content (e.g., random for compositional spread, or matched intergenic
for activity-range negatives) can break the plateau.

## Next
Experiment 008: cCRE + random 50/50 mix. Tests whether composition
spread (from random) and regulatory grammar (from cCRE) are additive
or one cancels the other.
