# 003_dinucleotide_shuffled

Take each 002 genomic 200bp window and shuffle it preserving dinucleotide
composition (Altschul-Erickson 1985 random Eulerian walk). Result has
the same length, base composition, and dinucleotide counts but motifs
and longer k-mer structure are destroyed.

## Result
mean across 14 evals: 0.463 (vs 002: 0.524, 001: 0.342)
eval_01: 0.436

## Decomposition of the genomic lift (001 → 002 = +0.15 on eval_01)
- 001 (uniform random):         0.343
- 003 (dinuc-shuffled genomic): 0.436 (+0.093 of the +0.154 lift = 60%)
- 002 (real genomic):           0.497 (full +0.154)

So **~60% of the genomic lift is explained by base composition +
dinucleotide statistics alone**. The remaining ~40% comes from higher-
order structure: motifs, longer k-mers, repeats, combinatorial grammar.

eval_08 is unchanged (~0.10) across all three libraries. It is
insensitive to anything in the genomic-vs-random axis.

## Implication for library design
Both axes matter:
- Matching natural sequence statistics (GC, dinuc) is "free" and gives
  ~60% of the lift.
- Real motif content gives the remaining ~40%.

The strategy for a high-scoring library: ensure natural composition
*and* enrich for motif content. ENCODE cCREs would be a natural
candidate for the next experiment.
