# 006_at_extreme

## Setup
50K random sequences with P(0)=P(3)=0.45, P(1)=P(2)=0.05.

## Results
**mean=NaN for all evals**, BUT condition_b and condition_c are defined:
- eval_01: cond_b=0.519, cond_c=0.400 (mean dragged to NaN by cond_a NaN)
- eval_07: cond_b=0.667, cond_c=0.538
- eval_13: cond_b=0.634, cond_c=0.504

Random had cond_a, b, c all defined for every eval.
Here cond_a is NaN for ALL evals → some constancy specific to cond_a's
view of the library when chars 1/2 are nearly absent.

## Key insights
1. **condition_a/b/c are real sub-evaluations**, each with its own
   correlation computation. mean = average of these.
2. cond_a requires diversity in chars 1 and 2 specifically (or evaluates
   a subset of positions/rows that becomes constant when 1/2 are rare).
3. Pushing AT-bias too far HURTS even condition_b/c relative to mild AT
   (exp 005). Sweet spot for eval_07 is around P(0,3)=0.35.
4. eval_01 cond_b: random 0.547 → AT-mild 0.565 (+0.018) → AT-extreme
   0.519 (-0.046). Peak somewhere near P(0,3)=0.35-0.40.

## Implication
Composition tuning has diminishing returns; eval_01 mean is stuck around 0.5
in the composition axis we've tested. Need to probe non-composition levers
(positional motifs, intra-sequence structure, row-index-correlated
properties).
