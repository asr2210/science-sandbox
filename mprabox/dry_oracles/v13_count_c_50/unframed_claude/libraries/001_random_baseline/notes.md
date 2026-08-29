# 001_random_baseline

## What
50,000 sequences of length 200, sampled uniformly i.i.d. over {A,C,G,T}.

## Why
Establish a zero-prior baseline. Discover output structure.

## Results
- mean_r ranges from -0.11 to +0.58 across the 14 eval sets.
- eval_01 (primary): 0.156 (k562=0.314, hepg2=0.033, sknsh=0.121)

### Eval pairs that are *identical* values (same metric, redundant slots):
- (eval_01, eval_14) → mean 0.156
- (eval_02, eval_05) → mean 0.1547
- (eval_03, eval_12) → mean 0.1042
- (eval_04, eval_09) → mean 0.4056
- (eval_06, eval_11) → mean 0.1451

So 14 evals collapse to ~9 unique signatures: {01,14}, {02,05}, {03,12}, {04,09}, {06,11}, {07}, {08}, {10}, {13}.

## Key observations
- Values look like Pearson r (range ≈ [-1, 1]).
- K562_r is remarkably *stable* across most eval sets at ~0.30–0.32 even with pure random sequences. Suggests the K562 component of every eval set agrees with the underlying "ground truth" model on random sequences.
- HepG2_r and SKNSH_r vary widely (-0.33 → +0.79), suggesting different evals measure different facets.
- eval_07 and eval_13 give *negative* hepg2/sknsh r → these eval models may have **inverted sign** convention or are anti-correlated with the ground truth on random.
- eval_08 mean 0.58 (with hepg2=0.76, sknsh=0.80) — extraordinary for random input.

## Interpretation
The metric is almost certainly a Pearson correlation between two predictions (or measurements) computed *over my 50K sequences*. To maximize r we need:
1. Sequences whose two predictors strongly agree → biological signal aligned features.
2. A spread of activities (not all-same, otherwise r → 0).

Random sequences already give r=0.16 on eval_01. The high score on eval_08 (0.58) suggests it may be sensitive to a simpler signal (e.g., GC content).
