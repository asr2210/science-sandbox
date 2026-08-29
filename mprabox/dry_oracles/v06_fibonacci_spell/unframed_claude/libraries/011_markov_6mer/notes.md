# Experiment 011: 6-mer Markov chain trained on hg38

## Plan
Train conditional P(next | 5-mer) on full hg38 (~2.9B transitions), generate
50k sequences. Tests whether 5th-order Markov captures the score-relevant
content of real DNA.

## Result
- eval_01 mean_r = **0.1279** (K562=0.028, HepG2=0.165, SKNSH=0.191)
- WORSE than even dinuc shuffle of real sequences (0.1326)
- Much worse than real genome random (0.1387)

## Implication
Markov-generated sequences match GLOBAL 6-mer statistics but don't reproduce
LOCAL clustering. A real 200bp genome chunk might have a few specific repeats
or CpG islands, which the Markov chain averages away. The score values
LOCAL coherence within each sequence, not just global k-mer matching.

This suggests that to do better than genome random, I'd need either:
- Sequences that are real genome chunks (already at ceiling for that)
- Sequences from sources matched to the test distribution

## Theory update
T8 refined: the scorer rewards both global composition AND local within-sequence
coherence. Synthetic Markov sequences lose the latter. Real genome chunks have
both, hence remain the best source.

## Next
Try cell-type-specific DNase peaks (K562/HepG2/SKNSH) — if the test sets are
biased toward accessible regions, this could improve over random genome.
