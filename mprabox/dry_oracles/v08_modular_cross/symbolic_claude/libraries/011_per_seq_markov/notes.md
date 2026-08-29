# 011 per_seq_markov

50,000 sequences, each from its own Dirichlet(0.5)-sampled 4x4 Markov transition matrix.
Diversifies dinucleotide stats across the 50k (not just monomer composition).

## Result
eval_01 = -0.0028. Mostly negative across evals (only eval_10 +0.0020).

## Interpretation
Dinucleotide diversity HURTS vs simple monomer diversity (Dirichlet). The Markov
structure constrains sequences differently than per-position Dirichlet sampling,
and the model doesn't reward this.

## Updated theory for eval_01
- condition_b loves randomness (random/Dirichlet best, ≈+0.007)
- condition_c likes diversity/motifs (Dirichlet/motif positive)
- condition_a likes strong repetition (4-mer repeats +0.002) but NEUTRAL for random/Dirichlet
- Goals contradict → cannot maximize all simultaneously
- Pure Dirichlet(0.5) is best balanced compromise (+0.0030)

## Next
Test Dirichlet(0.1) - more extreme compositions.
