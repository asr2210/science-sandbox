# 014 — 8 buckets cycling poly-X (0,1,2,3,0,1,2,3)

- 6250 strings per bucket. Compare to exp 005 (4 buckets ×12500): 0.0061.
- mean_r eval_01: 0.0036. Lower.
- 4-bucket cycle once > 8-bucket cycle twice for eval_01.
- Conclusion: 4 distinct buckets is the sweet spot for this design.
