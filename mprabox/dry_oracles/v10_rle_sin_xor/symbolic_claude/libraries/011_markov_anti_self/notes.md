# Experiment 011: Markov Anti-Self (STAY=0.20)

## Setup
- Markov chain with STAY=0.20 (slightly less than uniform 0.25)
- Marginals balanced; self-pair dinucleotides slightly under-represented

## Results
- eval_01: mean=0.5033, a=0.9548, b=0.5549, c=0.0002
- vs random: 0.5174, 0.9945, 0.5643
- Drop in a (0.95 vs 0.99), slight drop in b
- c unchanged

## Interpretation
- STAY=0.25 (uniform random) is the sweet spot for condition_a
- Both higher (STAY=0.55: a=0.72) and lower (STAY=0.20: a=0.95) hurt
- Symmetric optimum
