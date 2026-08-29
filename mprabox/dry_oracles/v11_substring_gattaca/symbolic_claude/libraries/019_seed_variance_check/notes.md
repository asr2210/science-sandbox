# 019 seed_variance_check

Identical recipe to 009 ([43,57] uniform-tuples + shuffle) but rng seed=7.

Result: eval_01 mean_r = **0.8675** (vs 0.8820 for seed=42). Noise = 0.015!

CRITICAL FINDING: single-seed run-to-run noise is ~0.015. Many of my "ranked
improvements" may have been within noise. Concretely:
- 009 (seed=42): 0.882
- 019 (seed=7):  0.868
- 011 [42,58]:   0.877  (could be ~equivalent to 009)
- 015 multinomial: 0.877 (could be ~equivalent)
- 017 marginal:  0.875  (could be ~equivalent)

Action: prioritize variance-reduction (stratified sampling, more deterministic
recipes). Need to find recipes that score robustly high.

Note conditions:
seed=42: a=0.856, b=0.909, c=0.881
seed=7:  a=0.848, b=0.910, c=0.844
c is the most variable (Δ=0.037). a slightly variable. b stable.
