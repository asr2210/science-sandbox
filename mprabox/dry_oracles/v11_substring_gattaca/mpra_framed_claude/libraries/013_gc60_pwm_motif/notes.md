# 013 GC=0.60 + PWM motifs λ=3

50k random GC=0.6 background + ~3 PWM-sampled JASPAR motifs per sequence.

## Result
- mean_r = 0.847 (eval_01 = 0.856)
- Below GC=0.6 alone (0.857)
- Same -0.010 penalty for motifs as at GC=0.5 (exp 006 vs 001: 0.842 vs 0.852)

## Takeaway
Motif penalty is consistent across GC backgrounds. The model robustly fails to
use motif signal. Lever is dead.

Next: try a different feature class — dinucleotide (CpG) enrichment via
Markov chain.
