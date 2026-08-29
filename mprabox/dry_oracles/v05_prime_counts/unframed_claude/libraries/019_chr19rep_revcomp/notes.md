# Experiment 019 — chr19 repeat-only + rev-comp augmentation

## Method
25K chr19 repeat-only + 25K rev-comp = 50K. Same composition,
double strand diversity.

## Results
- eval_01: 0.0481 (chr19 repeat: 0.0518) → slightly WORSE
- avg: ~0.045

## Interpretation
Rev-comp doesn't help. Strand axis isn't the variance lever.

## Next
EXP 20: same library with different seed → noise check.
