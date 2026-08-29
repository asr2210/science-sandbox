# Findings so far (exps 001-006)

## Ranked library scores on eval_01
- 005 hybrid genomic+cCREs    0.502
- 002 random genomic windows  0.497  ← natural-data plateau
- 003 dinuc-shuffled genomic  0.436
- 004 cCREs                   0.386
- 001 uniform random          0.343
- 006 motif-injected random   0.307  ← injection hurt

## Strong invariants
1. **Distribution match wins.** Libraries whose sequence distribution
   approximates "broad natural human DNA" score ~0.50. Any departure
   (uniform random, cCRE enrichment, consensus motif injection)
   scores lower.
2. ~60% of the random→genomic lift comes from base composition +
   dinucleotide statistics (compare 001/003/002).
3. ~40% comes from higher-order motif/structural content — but ONLY
   when those motifs sit in natural genomic context, not when injected
   into random backbones.
4. Curation toward regulatory elements (cCREs) HURTS — the model
   then can't predict the broader natural distribution.
5. Consensus-motif injection HURTS — model overfits to a bimodal,
   OOD activity distribution.

## eval_08 anomaly
eval_08 is stuck at 0.07-0.11 across every library. Insensitive to
naturalness, motif injection, etc. Hypothesis: it measures something
qualitatively different (saturation-mutagenesis variants? specific
TF-driven elements? very-low-SNR data?). Need to investigate
separately.

## eval-pair duplicates (4-decimal precision, all exps)
- 01 ≡ 14
- 02 ≡ 05
- 03 ≡ 12
- 04 ≡ 09
- 06 ≡ 11
Effective number of distinct evals = 9.

## K562 ≡ HepG2 (consistent across all exps)
The eval harness returns identical k562_r and hepg2_r values for
every library. Either it's collapsing the two reports, or these two
cell types are highly correlated in the model output.

## Practical recipe for a high-scoring library
Default: 50k random 200bp windows from a broad sample of GRCh38
autosomes, N-free. Tighter goals (e.g. eval_04) may benefit from
cCRE enrichment, but at cost to others. Avoid synthetic injections.
