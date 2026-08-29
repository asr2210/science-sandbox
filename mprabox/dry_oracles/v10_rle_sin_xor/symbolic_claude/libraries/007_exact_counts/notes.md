# Experiment 007: Exact per-sequence base counts

## Setup
- Each sequence = random permutation of exactly 50 of each base
- Removes per-sequence compositional variance

## Results
- eval_01: mean=0.2942 (DOWN from 0.5174), a=0.9921, b=-0.1112, c=0.0017
- a barely changed
- b CRASHED from 0.56 to -0.11
- c still ~0

## Interpretation
- Critical finding: condition_b rewards NATURAL per-sequence compositional VARIANCE
- Random sequences have natural ±6 variance in per-base counts (50 ± 6)
- Removing this variance with exact balance hurts b severely
- So condition_b is in a Goldilocks zone — i.i.d. uniform sampling is near-optimal
- Either too much bias (exp 002) or too little variance (exp 007) hurts b
