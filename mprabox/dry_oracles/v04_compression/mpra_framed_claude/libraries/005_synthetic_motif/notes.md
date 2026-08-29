# 005_synthetic_motif — notes

## Design
50K sequences of: 40%-GC random background + 3 distinct JASPAR vertebrate
PWM samples inserted at random non-overlapping positions.

## Result
- eval_01 = 0.1548 — **WORSE than random uniform (0.31)!**
- Most evals collapsed to 0.04-0.18 range
- Only eval_07 (0.38) and eval_13 (0.30) survived; both were "easy" evals
- eval_08 = 0.044, eval_04 = 0.044 — devastating

## Diagnosis
Synthetic library is *adversarial to a natural-DNA-trained model*:
- Random background has unnatural dinucleotide frequencies (no CpG depletion,
  no natural k-mer co-occurrence)
- Motifs placed at random positions with no natural co-occurrence patterns
- 3 motifs per sequence regardless of natural regulatory density
- Total absence of natural context (introns, repeats, CpG islands)

The model trained on this learns features specific to the unrealistic
distribution. When evaluated on natural-distribution test sequences,
those features don't transfer.

## Theory update (T3)
**Motif content alone is insufficient.** Natural sequence context (not just
the motifs in it) is what carries the most learnable signal. Synthetic
motif-rich sequences without that context are *worse than random*.

Restating: a library is informative if the *full distribution* of its
sequences matches what the eval distribution looks like. Mismatched
distributions (cCRE-only, synthetic-only) hurt regardless of how much
"regulatory information" they nominally contain.

## Generalization implication
For cross-cell-type generalization, the library should look like the
*genome-wide regulatory landscape* — which is exactly natural DNA. Any
distribution shift away from that hurts the model's ability to predict
unseen cell types, because those cell types operate on the same genomic
substrate.

## Next test
**Motifs embedded in natural background, not random background.** Take
50K natural genomic windows and insert 1-3 JASPAR motifs into each at
random positions. If model improvement comes from motif augmentation, this
should beat pure natural. If natural already contains sufficient motif
diversity, this should be neutral or harmful.
