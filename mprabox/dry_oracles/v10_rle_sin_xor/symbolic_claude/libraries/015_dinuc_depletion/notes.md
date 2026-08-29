# Experiment 015: Dinucleotide '12' Depletion

## Setup
- Doubly-stochastic Markov, P[1][2]=0.10 (vs 0.25 uniform)
- Marginals stay uniform; '12' dinucleotide depleted to ~2.5%

## Results
- eval_01: mean=0.5076, a=0.9549, b=0.5637, c=0.0042
- a dropped (0.99 → 0.95) — dinuc bias hurts k-mer uniformity
- b stable
- c slightly positive but within noise

## Interpretation
- Mild dinucleotide depletion doesn't help c
- Hurts a more than it helps anything
- Confirms: nothing beats pure random uniform structurally
