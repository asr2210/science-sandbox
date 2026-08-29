# 010 — 4-bucket motif at position 0 (start)

- Same as exp 005 (4 buckets, poly-X len 20) but motif at pos 0-19.
- mean_r eval_01: -0.0035 (down from +0.0061 in exp 005).
- BUT eval_13 jumped to +0.0097 (highest single value yet!).
  eval_08: +0.0069 (was -0.0012 in exp 005).
- Conclusion: motif POSITION matters and different evals favor
  different positions.
  - eval_01, 02, 06, 11 → favor middle (pos 90)
  - eval_04, 08, 13 → favor start (pos 0)
- For primary metric (eval_01): keep motif in middle.
