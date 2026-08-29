# Exp 013 — 40K random hg38 + 10K cCRE-centered

## Design
40K random 200bp windows from all main chromosomes + 10K cCRE-centered
windows (uniform across types). Shuffled together. GC=0.424; CpG=0.0118.

## Result
**eval_01 = 0.0493.** Essentially tied with 010 (random hg38 allchr, 0.048)
and 003/007 (random hg38 3chr, 0.049/0.052).

| eval | 010_allchr | 013_enriched |
|------|------------|--------------|
| 01 | 0.0480 | 0.0493 |
| 07 | 0.0331 | 0.0348 |
| 08 | 0.0395 | 0.0432 |
| 13 | 0.0376 | 0.0363 |
| mean | 0.0446 | 0.0451 |
| HepG2 mean | 0.0526 | 0.0535 |

## Interpretation
Light cCRE enrichment doesn't break the natural-DNA ceiling. Marginal HepG2
lift (+0.001) is below noise (~0.003). The 0.05 plateau on eval_01 is robust
to all reasonable mixtures of natural sequences.

## Theory update
Confirms: within the natural-DNA universe, library composition shifts can
move the score by ≤noise. The bottleneck is something orthogonal to "how
naturalistic" or "how regulatory-enriched" the sequences are.

## Next step
Try strand augmentation: 25K random hg38 windows each appearing twice
(forward + revcomp). DNA TF binding is largely strand-symmetric. If the
model doesn't internally augment, explicit RC pairing could double the
effective motif coverage.

## Time
46s wall, 15s evaluator.
