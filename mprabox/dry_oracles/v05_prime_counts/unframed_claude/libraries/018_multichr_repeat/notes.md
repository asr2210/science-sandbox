# Experiment 018 — Multi-chr (1+19+22) repeat-only

## Hypothesis
Adding chr1 + chr22 repeats to chr19 repeats increases repeat-class
diversity → higher r than chr19 alone (0.0518).

## Method
17K repeat-only windows from each of chr1, chr19, chr22; shuffle,
take 50K.

## Results
- eval_01: 0.0484 (chr19 repeat-only: 0.0518) → WORSE
- avg: ~0.044

## Interpretation
Adding chr1/chr22 repeats HURT slightly. chr19 specifically has
something better than the average — possibly Alu-richness
(chr19 is ~25% Alu, ~2x genome average) or higher GC% (~48% vs
genome ~41%).

## Theory update — T12
The 0.0518 ceiling is chr19-specific. Bigger pool ≠ better.
chr19 has the right COMPOSITION + DIVERSITY balance.

## Next
EXP 19: chr19 repeat-only + reverse-complement augmentation.
25K chr19 repeat-only + their 25K rev-comp = doubles strand
diversity but keeps composition. Tests if strand-axis variety
boosts r without changing composition.
