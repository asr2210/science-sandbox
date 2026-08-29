# 006_natural_plus_motif — notes

## Design
50K natural genomic windows (chr1-22, X, Y), each with 1-2 JASPAR
vertebrate motifs sampled from PWMs and inserted at random
non-overlapping positions, overwriting underlying bases.

## Result (28s training, 61s wall)
- eval_01: 0.4701 — **slightly worse than pure natural (0.480)**
- All evals within 0.01-0.02 of pure natural; pattern almost identical
- eval_08 still 0.09

## Interpretation
Motif insertion on top of natural background neither helps nor hurts much.
Slight reduction is consistent with mild distribution shift (motifs in
non-natural neighborhoods slightly distort co-occurrence patterns).

Comparison:
- 002 pure natural: 0.480
- 004 natural+cCRE 50/50: 0.494
- 006 natural+inserted motifs: 0.470

So adding *real* cCRE sequences (which are naturally regulatory in their
full context) > adding *synthetic* motifs to natural backgrounds.

## Theory implication
The model values NATURAL CONTEXT EVERYWHERE — including the motif's own
flanking sequence. Inserting motifs into wrong neighborhoods is mildly
adversarial. Better to add naturally-occurring regulatory regions
(cCREs) than to engineer them artificially.

## Next test
Either: optimize natural/cCRE ratio (cheap), or pursue orthogonal axis
(multi-cell-type DHS, augmentation).
