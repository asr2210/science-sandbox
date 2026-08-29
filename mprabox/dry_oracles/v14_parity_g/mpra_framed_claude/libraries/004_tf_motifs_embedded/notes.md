# 004 — Random background + embedded canonical TF motifs

Each sequence: 200bp random A/C/G/T + 1-6 consensus motifs (25 TFs across K562/HepG2/SK-N-SH and ubiquitous) placed at random positions, random orientations.

**Predicted:** Positive mean_r (0.1-0.4). Strong canonical motifs should drive learnable simulator signal.

**Got:** mean_r ≈ 0 (range -0.0075 to +0.0025). NO signal.

**Major theory contradiction.** The simulator does not respond to consensus motif insertions in random background, at least not in a way that generalizes to the eval sets.

**Next:** Try real MPRA-style libraries — sequences that look like what published MPRA papers actually use.
