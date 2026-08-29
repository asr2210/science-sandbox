# 004 — exact uniform composition per sequence

Each of 50,000 sequences has exactly 50 of each {0,1,2,3} in random order.

## Result
- eval_01: mean_r = 0.3077 (vs 0.4200 baseline) — WORSE
- a = 0.4312, b = 0.4736, c = 0.0183 (c sharply down vs 0.053 baseline)

## Interpretation
Enforcing strict balance is WORSE than iid random. Per-sequence composition
variance is ZERO here, vs ~6.1 std for iid random.

Confirms: per-sequence variance in some feature matters. Removing variance
in composition removes correlation signal.

eval_08 is reversed (slightly UP: 0.36 vs 0.38), suggesting eval_08 may
reward strict balance specifically. But it's an outlier.
