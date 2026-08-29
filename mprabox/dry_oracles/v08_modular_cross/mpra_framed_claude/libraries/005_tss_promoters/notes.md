# Experiment 005 — TSS-centered RefSeq promoter windows

## What I tested
50,000 windows of 200 bp centered on RefSeq transcript TSSs (41,527
unique TSSs, cycled). Strand-corrected (reverse complement on '-'
strand) so the 'transcription' direction is always 5' → 3'.

## Hypothesis
Promoters are universally strong in MPRA assays because they evolved
to recruit Pol II. They should give the model a robust signal across
all cell types — at minimum, HepG2 (many housekeeping liver-active
promoters).

## Result
- eval_01 = -0.0004 (still ~zero on mean)
- BUT HepG2-specific signal jumped on multiple evals:
  - eval_13: HepG2 = 0.0170 (highest so far for HepG2)
  - eval_12: HepG2 = 0.0114
  - eval_03: HepG2 = 0.0114
  - eval_07: HepG2 = 0.0101
- K562 was flat or slightly negative on most evals.
- SKNSH was uniformly slightly negative.

## What this tells me
**Different libraries activate signal in different cell types.**
- Exp 004 motif scaffold → K562 signal (hematopoietic motifs)
- Exp 005 promoters → HepG2 signal (liver-expressed housekeeping)
- Nothing has lit up SKNSH so far.

The mean_r metric is bounded by the WEAKEST cell type. To raise mean,
need a library that delivers signal in all three.

## Updates to theory
- Cell-type-specific signal is achievable with the right sequence
  content — confirms the model can learn cell-type-specific
  associations.
- The mean metric will require a **combined / diverse** library that
  has activating content for each cell type.
- SK-N-SH is consistently negative — possibly the model is missing
  neural-specific motifs, or SK-N-SH has low overall MPRA activity.

## Next
Hybrid library combining motif scaffolds (K562 boost), promoters
(HepG2 boost), and neural-targeted motifs (SK-N-SH).
