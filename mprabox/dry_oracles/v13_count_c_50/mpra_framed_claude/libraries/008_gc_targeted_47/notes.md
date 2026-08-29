# Experiment 008 — GC-targeted natural (44-52%)

## Design
Sample 50k 200bp windows proportional across all 24 chroms but REJECT
unless local GC in [0.44, 0.52]. Final mean GC = 0.477, std = 0.024.

## Results — massive negative
| eval | multi-chrom-5 | all-chrom | GC-targeted (this) |
|------|---------------|-----------|--------------------|
| 01 ★ | **0.555** | 0.509 | 0.259 |
| 03 | 0.560 | 0.524 | 0.245 |
| 04 | 0.509 | 0.397 | 0.348 |
| 07 | 0.628 | 0.638 | 0.130 |
| 08 | 0.021 | -0.124 | 0.331 |
| 10 | 0.501 | 0.459 | 0.186 |
| 13 | 0.614 | 0.622 | 0.126 |

## What I got wrong
Theory v7 said "match the sweet spot GC ≈ 47%." Implementing that by
narrowing the GC distribution to a tight band CRIPPLED the model.

## Theory v7 → v8: it's variance, not position
The library's compositional VARIANCE matters more than its position in
compositional space. By compressing GC variance to 0.024 (vs natural
~0.05), I gave the model no compositional gradient to fit. The model uses
GC variation as a major predictive feature; remove the variation and the
feature is useless.

This unifies every prior result:
- All libraries with broader compositional variance scored better
- Curated libraries (cCRE — narrower) lost on grammar evals
- GC-targeted (this — narrowest) lost catastrophically

Active learning literature insight applies: train data should COVER the
test distribution, not concentrate at the mode.

## Why eval_07/13 dropped to ~0.13
eval_07 and eval_13 reward broad genomic diversity (highest scores in
multi-chrom and all-chrom). Compressing GC variance eliminated that
diversity → the model can no longer discriminate the high vs low activity
classes that those evals reward.

## Implication
- Keep WIDE compositional support.
- Add motif content (natural sequences).
- Don't compress any axis of natural variation.
