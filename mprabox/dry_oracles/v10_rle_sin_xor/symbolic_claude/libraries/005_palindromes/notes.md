# Experiment 005: Reverse-complement Palindromes

## Setup
- Each sequence = first 100 random + reverse-complement (assuming 0<->3, 1<->2)
- All 50000 are palindromic
- Marginal composition: 25% each base

## Results
- eval_01: mean=0.3452, a=0.9949, b=0.0484, c=-0.0076
- a UNCHANGED at 0.99 (palindrome's k-mer distribution still uniform-looking)
- b CRASHED 0.56 → 0.05 (palindromes break b strongly)
- c stayed near 0

## Interpretation
- condition_a is content/structure tolerant as long as k-mer distribution remains uniform
- condition_b strongly disfavors palindromic structure — likely measures something
  about sequence "naturalness" or asymmetric features
- Palindromes are a dead end for boosting overall score
- Useful info: a and b can be decoupled — palindromes save a but kill b
