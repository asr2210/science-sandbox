# Experiment 012 — Mixed: 25K chr19 + 25K uniform random

## Hypothesis
Different evals reward different distributions. Mixing might serve
eval_08 (loves random) AND others (slightly prefer chr19).

## Method
25K chr19 200bp windows + 25K uniform random sequences, shuffled.

## Results
- eval_01: 0.0483 (chr19: 0.0502) → slightly WORSE
- eval_08: 0.1048 (chr19: 0.0551, random: 0.1237) → MUCH higher than chr19
- avg over 14: ~0.0496 (chr19: 0.048, random: 0.046) → slightly better

## Interpretation
Mixing serves the AVERAGE — eval_08 stays high while others stay
close to chr19's level. But the PRIMARY metric eval_01 went down
slightly because half the library is now random uniform (worse on
eval_01).

Tradeoff confirmed: pure chr19 wins eval_01; mixes win average.

## Next
Hypothesis: motif density variation across library could create
informative signal that both correlation axes track. Try chr19
backbone with VARIABLE TATA box density (0-10 per seq).
