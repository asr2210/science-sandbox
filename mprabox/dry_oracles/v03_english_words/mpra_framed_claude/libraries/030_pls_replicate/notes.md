# 030 — 012 recipe replicate with SEED=50 (3rd noise data point)

eval_01 = **0.4133**. K562 0.582, HepG2 0.608, SK-N-SH 0.050.

**Critical finding — true noise floor is ±0.006.**

3-seed view of the "012 recipe" (random + 1x25bp PLS):
| Seed | eval_01 | K562 | HepG2 | SK-N-SH |
|---|---|---|---|---|
| 12 (012) | 0.4248 | 0.591 | 0.619 | 0.065 |
| 50 (030) | 0.4133 | 0.582 | 0.608 | 0.050 |
| 100 (025) | 0.4225 | 0.584 | 0.613 | 0.071 |

Mean = 0.4202, range = 0.0115, stdev ≈ 0.006.

**Implications for the entire experiment series.** Many "012 lost to X" or "012 beat X" conclusions are within noise:
- 027 (400bp window, 0.4241), 028 (PLS+neural, 0.4232), 019 (PLS+TF mix, 0.4229), 022 (15bp PLS, 0.4211), 023 (18bp PLS, 0.4217) — all statistically indistinguishable from the 012 recipe's true mean.
- Clearly inferior recipes (below 0.420): pure random (0.4192 wait that's NOT inferior!), 014 (centered, 0.4196), 016 (pELS, 0.4201), 020 (motif-filtered, 0.4180), 024 (30bp, 0.4173), 015 (2x25bp, 0.4122), 026 (revcomp, 0.4155), 021 (48% GC, 0.4157), 029 (mix, 0.4209).
- The seed-12 result (012) was a lucky outlier; true mean is ~0.420 — barely above random's 0.4192.

**Theory v22 — the PLS-embed recipe gives ~0 mean improvement over random in expectation.** PLS embed gives +0.001-+0.005 mean lift in best case, lost in seed noise. The reproducibly strong recipes are: random (0.4192 ± small noise), PLS-embed (0.4202 ± 0.006), 400bp PLS (0.4241 ± likely similar). These three are within one noise SD of each other.

**Strategic implication.** For maximum eval score robustness, the ENSEMBLE recommendation would be a recipe like 012/027 (PLS 25bp embed, 200-400bp window). Single-best individual eval was 012's 0.4248.
