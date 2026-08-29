# Experiment 006: Random Baseline (Seed 43)

## Setup
- Same generator as 001 but seed=43

## Results
- eval_01: mean_r=0.5207 (vs 0.5174 seed=42), a=0.9944, b=0.5683, c=-0.0008
- Difference: 0.0033 between seeds

## Interpretation
- Scoring is reproducible (noise ~0.003-0.005 on eval_01 between random seeds)
- Just changing seed can give small gains (~0.005)
- Real signal needs to beat this noise floor
