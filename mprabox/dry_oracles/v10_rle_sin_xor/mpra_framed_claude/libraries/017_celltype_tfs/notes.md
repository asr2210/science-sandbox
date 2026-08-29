# 017 — cell-type-specific TFs (K562+HepG2+SK-N-SH) at fixed center

## Design
Filter JASPAR for 68 TFs known to be active in K562/HepG2/SK-N-SH (GATA1, TAL1, HNF4A, FOXA1, NEUROD1, SOX2, etc.). Insert 1 consensus at fixed center of random uniform background.

## Result
- eval_01 mean_r = **0.5130** (vs random uniform 0.5177, full JASPAR center 0.5191)
- K562 r = 0.9895 (slight drop)
- HepG2 r = 0.5617
- SK-N-SH r = -0.012

## Reading
Restricting to 68 cell-type-specific TFs HURTS vs all 870 motifs. Motif DIVERSITY matters more than RELEVANCE for this benchmark.

The hypothesis that targeted TF coverage would boost HepG2/SK-N-SH was wrong. Cell-type-specific motif insertion looks like overfitting bait.

## Implication
Stop trying to "match" the eval cell-type biology with restricted motif sets. Use full diversity. Going to test the narrow-GC seed=42 reproducibility next.
