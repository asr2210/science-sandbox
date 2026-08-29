# Experiment 008: Markov no-self-transitions

## Setup
- Markov chain: from any base, always switch to one of other 3 (uniform)
- Marginal composition balanced; dinucleotides 00,11,22,33 forbidden

## Results
- eval_01: mean_r=NaN, a=NaN, b=0.2805, c=0.0049
- a is NaN — condition_a's calculation FAILS when certain k-mers have zero count
- b dropped to 0.28
- c unchanged ~0

## Interpretation
- CRITICAL: condition_a is undefined for libraries where any dinucleotide has zero count
- Suggests a involves operations sensitive to zero counts (correlation with zero variance? log?)
- Constraint: keep ALL 16 dinucleotides (probably also all k-mers up to some depth)
  with positive frequency in library
- b sensitive too — moderately balanced dinucleotides matter
