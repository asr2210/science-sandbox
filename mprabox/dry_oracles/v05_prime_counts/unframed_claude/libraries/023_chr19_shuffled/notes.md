# Experiment 023 — chr19 within-window SHUFFLED

## Method
Each 200bp chr19 window: shuffle bases. Same per-seq composition,
no positional grammar.

## Results
- eval_01: 0.0387 (chr19 plain 0.0502) → LOWER by 0.011
- eval_08: 0.0781 (chr19 0.0551) → MUCH HIGHER

## Interpretation
Positional grammar contributes ~0.011 to chr19's eval_01 score.
Pure per-seq composition variance alone gives ~0.039.

eval_08 keeps showing a strong response to randomization /
variance, while eval_01 is the opposite.

## Update
Composition + position both matter for eval_01. Real chr19 has
both. Synthetic alternatives that preserve composition but not
position lose ~0.011.

## Next
EXP 24: chr19 plain with different seed — chase a lucky sample
at top of ±0.003 noise band.
