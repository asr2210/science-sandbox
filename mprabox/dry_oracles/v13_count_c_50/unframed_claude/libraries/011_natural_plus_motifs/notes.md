# 011_natural_plus_motifs

## What
50K natural hg38 sequences (chr1+chr22), with 0..6 strong activator motifs inserted at random positions, stratified by density.

## Why
Test if motifs help in a natural background (they hurt in random in exp 003).

## Results
eval_01: **0.5240** (vs random hg38 0.541, stratified natural 0.556) — hurts.
- K562_r: 0.575 (vs 0.581)
- HepG2_r: 0.493 (vs 0.541)
- SKNSH_r: 0.504 (vs 0.546)

## Interpretation
Motifs hurt even in natural backbone. The discrete motif insertions disrupt the natural compositional statistics that drive A/B agreement. Motifs are evidently NOT the right axis for this metric.

## Path forward
Try 2D stratification (GC × CpG) on natural to see if a second compositional axis adds variance beyond GC alone.
