# 007 markov_dna_like

50,000 first-order Markov sequences with human-DNA-like dinucleotide frequencies,
assuming 0=A, 1=C, 2=G, 3=T. Captures CpG depletion.

Stationary: A=0.274, C=0.239, G=0.228, T=0.259.

## Result
eval_01 = -0.0012 (slightly worse than baseline 0.0013).
**eval_07 spike: +0.0051** (condition_a = 0.0132).
eval_13 = +0.0030 (positive).
eval_10 = -0.0056 (worse).

## Interpretation
DNA-like structure helps SOME evals (07, 13) and hurts others (10, 03, 12, 04, 09).
For eval_01 specifically: small negative shift — DNA-like isn't great.

## Per-eval specialization emerging
- eval_01: rewards uniform diversity (random or Dirichlet best so far)
- eval_07: rewards DNA-like structure
- eval_10: rewards 4-mer repeats
- eval_13: rewards DNA-like

Different evals favor different sequence types.
