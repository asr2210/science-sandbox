# 008 — Period-4 interleaved motifs

- Each string i has poly-(i%4) motif at pos 90-109 (length 20),
  random uniform background. Compare to exp 005 (buckets of 12500).
- mean_r eval_01: 0.0053 (similar to exp 5: 0.0061).
- condition_a eval_01: **0.0107** (up from 0.0060 in exp 5).
- conditions_a are higher across most evals (eval_02,06: ~0.010,
  eval_08: +0.012 vs -0.003 in exp 5).
- mean_r similar because conditions b/c didn't gain.

## Interpretation
condition_a (the correlation) responds even better to high-frequency
arrangement (period 4) than to bucketed (period 12500). Suggests the
target has some structure varying fast in i. Test even higher freq next.
