# 004 bimodal

25k uniform random + 25k motif-rich (10 motifs each) shuffled.

## Results
- eval_01: mean=0.1242 (vs 0.1342 baseline) — worse
- K562 dropped (0.002 vs 0.010)
- SKNSH dropped (0.369 vs 0.382)

## Interpretation
Bimodal hypothesis rejected. Mixing random with motif-rich is even worse than
pure random. Three experiments with different content (motifs, GC, bimodal)
all reduce mean_r. Baseline uniform random remains best.

This suggests the scorer either:
1. Rewards a SPECIFIC distribution (close to uniform random) — anything that
   deviates from random hurts
2. Has a low ceiling that random already mostly saturates
3. Is checking some other property entirely (k-mer distribution, real-genome
   stats, length-related, etc.)

Next: try natural-genome-like sequences (Markov chain w/ dinucleotide bias).
