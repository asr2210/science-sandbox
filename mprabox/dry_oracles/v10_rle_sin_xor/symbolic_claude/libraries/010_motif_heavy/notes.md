# Experiment 010: Heavy Motif Insertion

## Setup
- 5 distinct balanced 8-mers per sequence at random non-overlapping positions
- 40 structured chars + 160 random per sequence

## Results
- eval_01: mean=0.5153, a=0.9877, b=0.5630, c=-0.0047
- Slight DROP from random baseline (0.5174)
- a hurt: 0.9877 vs 0.9945 (heavier motifs disturb k-mer uniformity)
- b basically unchanged
- c unchanged

## Interpretation
- Heavy motif insertion: small cost to a, no benefit elsewhere
- Confirms: motif content doesn't move c
- Best strategy may be: pure random with lucky seed
