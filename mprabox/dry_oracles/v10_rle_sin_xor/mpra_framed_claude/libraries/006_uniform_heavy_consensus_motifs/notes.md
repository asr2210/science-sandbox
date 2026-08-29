# 006 — random uniform + heavy CONSENSUS JASPAR motif insertions

## Design
Base random uniform 200bp. Each seq gets Poisson(6) ∈ [3,10] consensus-realized JASPAR motifs at random non-overlapping positions. Avg 6 motifs/seq, ~59 bp coverage per 200bp.

## Result
- eval_01 mean_r = **0.5055** — WORSE than random uniform (0.5177)
- K562 r = 0.9554 (vs 0.9946) — clear drop
- HepG2 r = 0.5674 (vs 0.5674) — IDENTICAL to baseline
- SK-N-SH r = −0.0062 — flat

## Reading
Even heavy consensus motif insertion failed to lift HepG2 or SK-N-SH by even a single percent. The 60bp of intentional motif coverage per sequence subtly disturbed composition (mostly preserved 0.49 GC but distribution different) and dragged K562 down to 0.96.

**Motifs are essentially invisible to this benchmark.** Combined with 005, this is now strong evidence: the model trained on the library can't extract useful signal from arbitrary JASPAR motif insertions for any of the three cell types in any of the 14 evals.

## Implication
Stop investing in motif insertion as a strategy. The lever must be elsewhere — possibly k-mer/dinucleotide patterns, sequence-specific structures (repeats, palindromes), real MPRA-tested sequences from existing datasets, or sequence patterns I haven't tried yet.
