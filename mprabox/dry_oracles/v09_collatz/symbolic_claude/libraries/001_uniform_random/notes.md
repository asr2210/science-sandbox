# 001 — Uniform random baseline

Each row is iid uniform from {0,1,2,3}, length 200, seed=42.

## Result
- eval_01: mean_r=0.2399 (a=0.1407, b=-0.0463, c=0.6253)
- All non-eval_08 mean_r ≈ 0.22-0.24
- eval_08 is an outlier (mean_r=0.087) — much harder

## Observations
- mean_r = (a + b + c) / 3 (arithmetic mean — verified)
- Condition c is consistently ~0.63 on random → may reward something
  generic about composition/diversity
- Condition b is slightly negative on random → opportunity to push it up
- Many eval sets appear identical (01==14, 02==05, 06==11, 03==12, 04==09)
- eval_07 and eval_13 differ in small ways from the 01-cluster
- eval_08 stands apart — likely uses a different metric or harder target
- eval_10 looks unique with a ≈ 0.12 (lower than 0.14)
