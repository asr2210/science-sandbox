# Experiment 004: Dinucleotide Repeat Insertions

## Setup
- 5 groups of 10000: 1 control + 4 motif groups
- Each motif group has a 10-char dinucleotide repeat (e.g., (01)*5) at random position

## Results
- eval_01: mean=0.5060 (vs 0.5174 random), a=0.9753, b=0.5406, c=0.0021
- Very small effect (slight drop)
- c didn't move (still ~0)

## Interpretation
- Small motif insertions barely change scores
- Slight cost to a (0.99 → 0.98) from local non-uniformity
- Slight cost to b
- c stubbornly near zero — dinucleotide repeats don't unlock it
