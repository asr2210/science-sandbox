# Exp 001: Uniform Random Baseline

## Setup
50,000 strings of length 200, each character uniform over {0,1,2,3}.
Seed=42.

## Result
eval_01 (primary): 0.2974
Highest: eval_07 = 0.4218
Lowest: eval_08 = 0.1047

## Observations
- For uniform random, condition_a == condition_b exactly in all eval sets.
  Could be (i) two identical metrics, (ii) symmetric metrics that
  coincide under uniform input, or (iii) symmetric halves.
- condition_c usually slightly differs (often higher).
- Several eval sets give IDENTICAL outputs on uniform random:
  eval_01 = eval_14 (0.2974)
  eval_02 = eval_05 (0.2975)
  eval_03 = eval_12 (0.3292)
  eval_04 = eval_09 (0.2862)
  eval_06 = eval_11 (0.3242)
- mean_r = (a + b + c) / 3 (verified: 0.2974 = (0.2940+0.2940+0.3042)/3).
- eval_07, eval_08, eval_10, eval_13 are unique.
- eval_08 very hard (0.105) — biggest headroom for improvement.

## Hypothesis after Exp 001
Alphabet of 4 letters and L=200 suggests this is DNA-style scoring
(e.g., MPRA: massively parallel reporter assay). condition_a/b/c may
correspond to different cellular contexts or replicates. 14 eval sets
could be different cell types or models. The fact that some are
identical pairs suggests redundant evaluation models.
