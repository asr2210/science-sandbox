# Scoring metric: Pearson correlation across library

The black-box scorer computes `r` per cell type per eval set across
the 50k sequences in the library. Confirmed by experiment 007
(all-identical library → NaN, i.e. zero variance breaks correlation).

## Implications
- The library must have variance in PREDICTED activity. Identical or
  near-identical sequences zero out the metric.
- A library with wide, well-aligned variance between the eval predictor
  and the implicit "ground truth" maximizes r.
- Uniform random already provides ~0.42 baseline because natural
  motif-presence variance correlates with the implicit ground truth.
- Strategy: bimodal / graded libraries where some sequences carry
  strong cis-regulatory features and others are quiet, with all
  sequences distinct.

## Things that REDUCE r
- Uniform composition skew (GC65, GC35) — pushes whole library OOD.
- Dinucleotide-Markov "real DNA" sampling — slightly worse than uniform.
- Sprinkling identical TF motifs on every sequence — compresses variance.

## Things to try
- Bimodal (random + motif-rich halves) for wider variance.
- Activity gradient (varying motif copy number across sub-populations).
- Cell-type-specific motif clusters (NRSE for SKNSH, GATA for K562, HNF for HepG2).
