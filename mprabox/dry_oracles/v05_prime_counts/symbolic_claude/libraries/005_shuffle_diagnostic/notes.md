# 005 — Shuffle diagnostic

## Setup
Same exact 50K sequences as exp 001 (uniform random seed=0), permuted with
seed=12345.

## Results
- ALL 14 evals returned IDENTICAL scores to exp 001, down to the 4 decimals reported.
- eval_01 = 0.0420, eval_08 = 0.1242, etc.

## Inference — CRITICAL
The scoring function is **permutation-invariant** on the input library. It does
NOT depend on the order of sequences in `sequences_0.txt`. mean_r is a
library-level / bag-of-sequences statistic.

This RULES OUT the "correlation against fixed index-aligned target vector"
hypothesis. The metric must be one of:
- Correlation between two model predictions on my library (per cell line)
- Correlation between predicted activity and some sequence-derivable feature
- Some library-level information / quality metric

The fact that random uniform gives r=0.042 and biased gives r=−0.022 is now
explainable: the library STATISTIC (e.g., correlation between two models'
predictions on the sequences I submitted) shifts as the sequences move
in/out of model-distribution.

## Implications for next experiments
- Order doesn't matter: I can sort, shuffle, group sequences freely with no
  effect on score
- The score rewards properties of the COLLECTION, not the alignment
- To improve, I need to find which library compositions make the two
  evaluation surfaces (whatever they are) agree more strongly
