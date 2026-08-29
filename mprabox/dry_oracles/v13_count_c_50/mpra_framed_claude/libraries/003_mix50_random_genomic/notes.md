# Experiment 003 — 50/50 random + random genomic

## Design
25,000 uniform random ACGT + 25,000 hg38 chr19 random windows, shuffled.

## Results
| eval | 001 random | 002 genomic | 003 mix50 |
|------|------------|-------------|-----------|
| 01 ★ | 0.1294 | **0.5260** | 0.4328 |
| 02 | 0.1281 | 0.5269 | 0.4336 |
| 03 | 0.0771 | 0.5143 | 0.4108 |
| 04 | 0.3902 | 0.5845 | 0.5331 |
| 06 | 0.1189 | 0.5234 | 0.4238 |
| 07 | -0.1416 | 0.4904 | 0.3253 |
| 08 | **0.5795** | 0.2921 | 0.4115 |
| 10 | 0.0938 | 0.4412 | 0.3307 |
| 13 | -0.1470 | 0.4786 | 0.3104 |
| **mean** | ~0.15 | **0.504** | 0.418 |

## Interpretation
The hybrid recovered eval_08 partially (0.29 → 0.41) but at the cost of
all grammar evals (e.g. eval_01 0.53 → 0.43). Net: worse than pure genomic.

The compositional gain on eval_08 (+0.12) does not compensate for the
grammar loss (-0.08 on average across 8 evals). The "library heterogeneity
helps" hypothesis is FALSIFIED in this simple form.

## What this means
- The model can't independently learn "if random, use composition; if natural,
  use grammar." It seems to average the two regimes, hurting both.
- Or: half the training data per regime is too little — the model needs more
  examples of natural sequences to learn the grammar.
- Either way: a 50/50 split is not the right answer.

## Theory update needed
The dual-axis model needs refinement. Three candidate refinements:
A) "Library purity" matters: a homogeneous distribution lets the model learn
   one consistent mapping. Mixing distributions confuses the gradient.
B) "More natural is more grammar": cut training data of genomic in half →
   grammar quality halved.
C) eval_08 requires a different *strategy* — not just compositional
   sequences, but specifically *out-of-distribution* sequences whose target
   is well-explained by simple features.

Next experiment should isolate (A) vs (B): does *adding* more genomic
diversity help (multi-chromosome) without compromising signal-to-noise?
