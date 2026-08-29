# Experiment 001: Random Baseline

## Setup
- 50,000 strings of length 200, uniform random {0,1,2,3}, seed=42

## Results
- eval_01: mean_r=0.5174, a=0.9945, b=0.5643, c=-0.0065
- Across evals: mean_r 0.47–0.53; eval_08 is consistently lower (~0.47)
- condition_a ≈ 0.99 across all evals (nearly saturated)
- condition_b ≈ 0.56
- condition_c ≈ 0 (no signal)
- Total time: 48.4s

## Interpretation
- mean_r = (a + b + c) / 3
- condition_a may be near-saturated regardless of content
- condition_c gives ~0 because random sequences don't capture the structured target
- biggest improvement opportunity: boost c (currently ~0) and b
- eval_08 stands out as harder
