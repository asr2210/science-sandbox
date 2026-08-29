# 002 — Per-seq composition bias (90% dominant base)

## Setup
For each of 50K sequences, choose dominant base uniformly from {0,1,2,3}; each
position is dominant base with p=0.90, else uniform over the other 3.
Result: ~4 equal sub-populations of "mostly-0", "mostly-1", "mostly-2", "mostly-3".

## Results
- eval_01 = **−0.0223** (vs baseline 0.0420). Δ = −0.064
- eval_08 = **−0.0322** (vs baseline 0.1242). Δ = −0.156 — biggest drop
- ALL evals went negative (range −0.013 to −0.032)
- time_s = 13

## Inference
1. Composition matters STRONGLY. Highly biased per-seq composition not only loses
   signal but actively anti-correlates with target.
2. eval_08 lost the most signal (drop of 0.156). Whatever eval_08 measures, it's
   especially sensitive to compositional homogeneity within a sequence.
3. Uniform random already captures useful signal; deviation from uniform hurts.

## Updated theory
mean_r likely measures correlation between model-predicted activities on my
library and some target (either a held-out activity vector or another model's
prediction). Random uniform composition keeps predicted activities in the range
the target model was trained on (positive correlation). Strongly biased
sequences fall outside that distribution → predictions go to "wrong" extremes
that anti-correlate with target.

This suggests that to maximize r, I want:
- Sequences that lie in-distribution for what the model was trained on
- Sufficient spread in activity (so correlation has signal to track)
- NOT compositional homogeneity within sequences
