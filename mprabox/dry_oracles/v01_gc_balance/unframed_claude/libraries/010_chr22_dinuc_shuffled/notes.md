# 010_chr22_dinuc_shuffled

chr22 sequences with per-sequence mononucleotide shuffle. Preserves per-seq
GC content distribution; destroys motifs and dinucleotide order.

## Result
eval_01: 0.5709 (vs 0.6780 chr22 real). -0.11 drop.
eval_07: 0.6858 (vs 0.7462). -0.06 drop.
eval_04: 0.3578 (vs 0.5809). big drop.
eval_08: 0.1556 (vs 0.1230). slight bump — eval_08 likes shuffled more!

## Interpretation
Motifs and higher-order structure DO matter (~0.11 of eval_01 from motif content),
but composition alone provides the bulk of the signal (~0.57 of 0.68).

Specifically: eval_04 cares a LOT about structure (-0.22 drop from shuffle).
eval_08 ANTI-correlates with structure — it prefers random/shuffled.

This suggests eval_08 may be diversity/entropy related or measuring something
adversarial (e.g., rewards low predictability).

## Implication
To push past 0.68 plateau on eval_01, motif content matters. Either:
- Cell-type accessible regions (DHS peaks)
- MPRA-tested sequences (best signal)
- Engineered motif insertion
