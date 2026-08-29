# 001 — Uniform random baseline

## Setup
50,000 iid uniform random strings of length 200 over {0,1,2,3}, seed=0.

## Results
- eval_01 = 0.0420 (primary)
- eval_08 = 0.1242 (outlier: ~3x baseline)
- Most evals ~0.02–0.05
- time_s = 38.7

## Observations
- Several eval sets give IDENTICAL scores → they are duplicates:
  - 01 == 14
  - 02 == 05
  - 04 == 09
  - 06 == 11
  - 03 == 12
  - 9 unique evals among 14
- eval_08 has noticeably higher floor (~0.12 across all cell types)
- mean_r values across cell types track each other within an eval set
- Random correlation noise floor for N=50K is ~0.0045, so 0.04 is well above noise.
  Uniform random sequences have *some* feature that aligns with target signal.
