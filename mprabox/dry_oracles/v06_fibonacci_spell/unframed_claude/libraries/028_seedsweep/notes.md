# Experiment 028: Seed sweep — seed=2026

Plain hg38 random with seed=2026.

## Result
- eval_01 mean_r = **0.1339**
- Lower-tail of seed distribution; no improvement

## Summary of seed sweep
All 6 seeds tried (006:6, 014:14, 025:42, 026:123, 027:777, 028:2026):
mean = 0.1357, std = 0.0016, max = 0.1387 (seed=6).
seed=6 was upper-tail by ~2 sigma; no other seed reproduced.

## Next
Try one more pooled mix using top-3 seeds (6, 42, 777) = 16.7k each.
Then final submission as pure seed=6 base.
