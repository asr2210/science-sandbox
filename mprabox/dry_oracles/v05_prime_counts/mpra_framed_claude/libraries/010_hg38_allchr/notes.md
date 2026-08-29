# Exp 010 — Random hg38 from all chromosomes

## Design
50K x 200bp random N-free windows sampled from all main chromosomes (chr1-22, X, Y)
weighted by length. GC = 0.409 (matches genomic mean perfectly).

## Result
**eval_01 = 0.0480.** Essentially tied with chr8/19/22 (seed=0 0.049, seed=1 0.052).

| eval | hg38_3chr_s0 | hg38_3chr_s1 | hg38_allchr |
|------|--------------|--------------|-------------|
| 01 | 0.0490 | 0.0523 | 0.0480 |
| 07 | 0.0320 | 0.0331 | 0.0331 |
| 08 | 0.0492 | 0.0473 | 0.0395 |
| 13 | 0.0336 | 0.0322 | 0.0376 |

eval_13 (hardest, most sequence-specific) is best yet at 0.038 — modest lift
from broader natural sampling, mostly in eval_13/07 (sequence-specific evals).

## Interpretation
Broader sampling doesn't lift eval_01 vs 3-chr sampling. The 3 chromosomes
were apparently representative enough of "natural DNA" for what the eval
measures.

But eval_13 IS better (0.038 vs 0.032). Suggests there's a small advantage
for libraries that span more diverse genomic contexts on the most
sequence-specific eval.

## Next step
Try a fundamentally different design: **saturation-mutagenesis-style
library**. Take a few hundred cCREs and generate many variants of each,
so the model sees the same biology at many activity levels (point
mutations alter activity slightly). This is label-informative library
design: the same context is queried at many points along the activity
axis.

## Time
14s evaluator, 45s wall.
