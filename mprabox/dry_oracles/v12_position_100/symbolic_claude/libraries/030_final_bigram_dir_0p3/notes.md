# Exp 030: Final — 4-seed bigram-Dir(0.3) mixture

## Hypothesis
The bigram-Dir(0.3) family is the best-scoring method (exp 010 = 0.0784).
But seed variance is high (±0.001-0.002): seed 23→0.0784, seed 151→0.0761,
seed 99→0.0769. Mixing seeds may stabilize toward the upper tail or just
average out near the mean.

## Method
12.5K seqs from each of 4 seeds {23, 42, 99, 1337}, shuffled. Includes the
proven-good seed=23 for upside.

## Result
eval_01 = 0.0779. Did NOT beat exp 010 (0.0784) but among the top 4. The
mixture pulled the score toward the bigram-Dir(0.3) population mean rather
than the seed=23 outlier.

## Interpretation
Confirms: seed=23 exp 010 is a +1.5σ lucky draw within the bigram-Dir(0.3)
distribution. The "true" population mean appears to be ~0.0770-0.0775.
Mixing seeds gives a more reliable score near the population mean.
