# 006_gc_cpg

## What
50K sequences from a first-order Markov chain. Per-sequence: GC ∈ [0.05,0.95], CpG O/E ∈ [0.05,3.0]. Joint variance via IPF on 4x4 dinucleotide matrix.

## Why
Test orthogonal CpG axis on top of GC.

## Results
eval_01: **0.4186** (vs 0.414 exp 5 → +0.005)
- K562_r: 0.489 (vs 0.472, +0.017)
- HepG2_r: 0.354 (vs 0.363, -0.009)
- SKNSH_r: 0.412 (vs 0.407, +0.005)

CpG axis adds essentially nothing on top of GC. K562 improves slightly. Plateau near 0.42 for compositional variance alone.

## Next
Try natural genomic sequences (real human enhancer-flanking regions) — they have multi-feature variance that models trained on real MPRA data should agree on more strongly than synthetic compositional sequences.
