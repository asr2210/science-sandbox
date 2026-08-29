# Experiment 002: GC-balanced random at 42% GC

## Plan
Sample bases with P(A)=P(T)=0.29, P(C)=P(G)=0.21 (~human genome composition).
Isolates GC effect from uniform 50% GC baseline.

## Result
- eval_01 mean_r = **0.1152** (K562=0.013, HepG2=0.159, SKNSH=0.174)
- Essentially unchanged from random 50% GC (0.1176)
- Slight reshuffle: HepG2 ↑, SKNSH ↓, mean similar

## Implication
First-order base composition does NOT meaningfully drive the score. Future
experiments should explore higher-order structure (motifs, k-mers, real
sequences, dinucleotide content).
