# Exp 011 — Saturation-mutagenesis on 500 cCREs

## Design
500 randomly selected cCREs (all types). For each, 1 original + 99 variants
spanning mild (1-2 mutations) to severe (16-40 mutations). 500 × 100 = 50K.
GC = 0.483.

## Result
**eval_01 = 0.0295 — worst natural-context library result yet.** eval_13 = 0.011
(near-zero).

## Interpretation
Wrong design choice. Saturation mutagenesis sacrifices sequence diversity
(only 500 distinct biological contexts) for label-informativeness (many
measurements per context). The model can't generalize from 500 contexts to
held-out sequences, even though it sees the same contexts at many activity
levels.

**Sequence diversity matters more than label-informativeness in this
black-box training setup.** With 50K near-duplicates, the model probably
learns context-specific quirks of those 500 cCREs and fails to transfer.

## Updated principle
**Independence of training sequences matters.** Near-duplicates within the
library shrink effective sample size. 50K independent samples beat 500
contexts × 100 mutants.

## Next step
Test whether the bottleneck is "real DNA itself" or "distribution match":
generate a synthetic library with hg38-matched 5-gram statistics
(higher-order Markov). If it ties random hg38 (~0.05), distribution is what
matters. If it falls short, the actual DNA carries information beyond
statistics.

## Time
12s evaluator, 44s wall.
