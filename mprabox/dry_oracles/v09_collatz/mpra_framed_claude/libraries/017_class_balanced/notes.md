# 017_class_balanced

## Design
1,000 cCREs from each of 5 primary classes × 10 random-offset tiles
each = 50K:
- PLS (40,891 available)
- pELS (172,027)
- dELS (789,200)
- CTCF-only (35,839)
- DNase-H3K4me3 (25,921)

Random cCRE sampling is 74% dELS-biased; class-balanced is a clean
1:1:1:1:1 archetypal split.

## Hypothesis (T11)
cCREs are 5 distinct regulatory archetypes. Balanced exposure
should expose the model to the full archetypal vocabulary,
which transfers better than a dELS-dominated random sample.

## Result vs 014 (5K x 10 broad cCRE)
                eval_01  K562    HepG2   SKNSH   eval_07  eval_13
014 5K x 10:    0.3181   0.144   0.188   0.623   0.337    0.328
017 class-bal:  0.3171   0.141   0.184   0.626   0.338    0.328

PARITY. Tiny SKNSH lift (+0.003), tiny K562/HepG2 drops.

## Interpretation
Class balancing is NEUTRAL. The plateau is class-agnostic. Whether
the 5K regions are 74%-dELS or 20%-each, the model lands at the
same place. Implication: regulatory ARCHETYPE diversity is not the
missing lever.

## Theory T11 (refined)
The plateau ~0.318 is set by per-cell-type addressable variance
under the architecture + 50K budget, AND is invariant to any
within-natural-genomic structural manipulation tested so far:
- Source modality (DHS, cCRE, STARR, conserved)
- Source quality (top-N, signal threshold)
- Cell-type stratification (per-cell-type, differential, shared)
- Class composition (random vs class-balanced)
- Per-region density (5, 10, 20, 50 tiles)
- Region count (1K – 50K within the 5K-saturation plateau)
- Strand augmentation (RC)
- Mutational pairing (sat-mut)

## Next
Experiment 018: MULTI-SOURCE SATURATION. Take 1K regions from each
of 5 different sources at saturating depth: cCREs / K562 DHS /
HepG2 DHS / SKNSH DHS / phastCons-conserved cCREs. 1K each × 10
tiles = 50K.

Tests: at saturating total region count (5K), does SOURCE diversity
(orthogonal evidence streams converging) lift the plateau? Each
source is an independent regulatory annotation; their union is
"things many lines of evidence agree are regulatory".

Generalization justification: multi-evidence regions are the
intersection of "what looks regulatory under many assays" — the
most defensible regulatory annotations, and the most likely to
represent universal regulatory grammar.
