# Exp 001 — Random uniform ACGT

## Design
50,000 sequences, 200bp, each base iid uniform over {A,C,G,T}. Seed 0.

## Result
mean of eval_01..14 mean_r ≈ 0.046. eval_01 = 0.042. Mostly noise.

Notable: eval_08 = 0.124 — markedly higher than the others. With no
predictive features in the inputs, that ~0.12 floor likely reflects the
evaluator/model picking up a population-level bias (e.g. GC, k-mer
counts) that correlates with eval_08 labels even from a random library.
Worth checking again later.

eval_13 is lowest (0.020) — probably the most sequence-specific eval.

## Interpretation
A trained model on random sequences has essentially no signal. Most evals
are near-zero correlation. This sets the floor: anything I design should
beat ~0.04 on eval_01.

The eval_08 anomaly is a clue that not all 14 evals weight features the
same way — some may reward dataset-level biases more than others.

## Time
11.5s evaluator time, ~55s wall (sequence gen + import overhead).
