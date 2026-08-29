# Experiment 003: Markov Runs (Higher-Order Structure)

## Setup
- Markov chain, self-transition prob 0.55, else uniform across other 3
- Marginal composition stays balanced (~25% each base)
- But dinucleotide distribution is biased toward self-pairs

## Results
- eval_01: mean_r=0.4083 (was 0.5174 random), a=0.7185, b=0.5058, c=0.0007
- a dropped 0.99 → 0.72 — condition_a is sensitive to HIGHER-ORDER randomness
- b dropped 0.56 → 0.51 — minor
- c still ~0

## Interpretation
- condition_a measures more than marginal composition; it cares about higher-order
  distribution (likely k-mer frequencies matching uniform)
- Truly random is near-optimal for a
- b is fairly stable as long as marginals are balanced
- c remains untouched by anything we've tried
