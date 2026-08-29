# 021 struct_only_variation

50k sequences, each = permutation of multiset (50x0, 50x1, 50x2, 50x3).
Composition IDENTICAL across all seqs; only structural permutation varies.

## Result
**ALL NaN** — model outputs were constant across all 50k sequences.

## MASSIVE INSIGHT
The model M(seq) depends primarily (perhaps entirely) on COMPOSITION,
not on structural arrangement. All structural variation collapses to
same prediction → constant → NaN.

This explains why no structural method (motifs, palindromes, blocks, Markov)
beat compositional methods (Dirichlet).

## New strategy
- Vary composition AGGRESSIVELY along specific axes.
- Maybe f(seq) depends on a specific composition projection
  (count of one char, GC ratio, etc.) that I haven't isolated.
- Try single-axis composition variation: vary count of char 0 only.
