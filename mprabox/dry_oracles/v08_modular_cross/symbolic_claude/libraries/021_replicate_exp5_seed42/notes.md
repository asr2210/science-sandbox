# 021 — Replicate exp 5 design with seed 42

- mean_r eval_01: 0.0010 (vs exp 5 seed 23 = 0.0061).
- HUGE seed variance! The 0.006 ceiling was largely lucky bg.
- Real motif signal is much smaller; bg randomness dominates.
- eval_07: 0.0051 (vs 0.0029 seed 23) — also seed-sensitive.
- Suggests we should DE-NOISE bg, e.g., share bg across buckets so
  motif difference is the only bucket-level difference.
