# 009 — Random motif identity per string

- Each string: random uniform bg + poly-X motif at pos 90 (length 20),
  X random per string from {0,1,2,3}.
- mean_r eval_01: 0.0020, condition_a 0.0054.
- DOWN from exp 8 (period 4) condition_a 0.0107.
- Conclusion: period-4 was a special frequency. Higher-frequency
  (random per string) doesn't help; reverts toward random baseline.
