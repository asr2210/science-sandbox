# Experiment 028 — Synthesis library (best-of-all learnings)

## Design
50K = 5 GC bins × 10K. Within each bin: 4 sources × 2500:
- 2500 hg38 natural (GC-binned)
- 2500 mm39 natural (GC-binned)
- 2500 hg38 DHS-anchored (GC-binned)
- 2500 hg38 cCRE high-conf (GC-binned)

Combines: GC strat (T8), multi-source (T10), multi-genome (T4).

## Result
- eval_01: 0.3941
- K562: 0.6063, HepG2: 0.4299, SK-N-SH: 0.1462

## Comparison to ceiling cluster
| design | eval_01 |
|---|---|
| 4-way mix seed 0 (002) | 0.3937 |
| 4-way mix seed 1 (010) | 0.3961 |
| 4-way mix seed 2 (022) | 0.3954 |
| GC-strat natural (014) | 0.3939 |
| GC + reg (015) | 0.3945 |
| multispecies GC (020) | 0.3947 |
| **synthesis (028)** | **0.3941** |

Within noise (σ=0.0012) of GC-strat alone and 4-way mix mean (0.3951).

## Interpretation
**Combining all positive levers does NOT exceed any single one.**
GC-strat × multi-source × multi-genome ≈ GC-strat alone ≈ 4-way mix.
The 0.395 ± 0.002 ceiling is hard.

This confirms T10 in the strongest form: once GC is balanced, no
combination of source/genome diversity adds further information.
All paths converge to the same ceiling.

## Implication for next exp (029)
Run synthesis with seed=1 to get a noise estimate on this complex
design. If close to 0.3941, confirms within-design noise; if far,
the design is unstable and seed-sensitive.
