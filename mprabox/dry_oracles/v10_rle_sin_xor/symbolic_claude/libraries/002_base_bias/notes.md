# Experiment 002: Single-Base Bias Probe

## Setup
- 4 groups of 12500, each ~80% one base, ~6.67% others
- Library covers all 4 single-base biases

## Results
- eval_01: mean_r=0.0916 (was 0.5174 random), a=0.6347, b=-0.3591, c=-0.0007
- All evals dropped to ~0.09
- condition_a fell 0.99 → 0.63 (composition matters)
- condition_b went negative (active penalty)
- condition_c unchanged at ~0
- Time fell 48s → 14s (interesting — maybe faster forward pass?)

## Interpretation
- Library-level composition matters strongly
- Balanced random is much better than per-sequence biased
- Cannot win by enriching for any single base
- Keep marginal base composition balanced (~25% each)
