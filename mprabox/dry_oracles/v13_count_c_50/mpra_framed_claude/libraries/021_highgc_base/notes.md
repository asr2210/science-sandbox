# Experiment 021 — high-GC base library (chr16/17/19/20/22)

## Result vs 013 (mc5 base)
| eval | 013 (mc5) | 021 (high-GC) | Δ |
|------|-----------|---------------|---|
| 01 ★ | **0.5765** | 0.5447 | -0.032 |
| 04 | 0.5774 | **0.5973** | +0.020 |
| 07 | **0.6037** | 0.5154 | -0.088 |
| 08 | 0.1730 | **0.2986** | **+0.126** |
| 10 | **0.5087** | 0.4610 | -0.048 |
| 13 | **0.5865** | 0.5014 | -0.085 |
| mean8 | 0.5705 | 0.5421 | -0.028 |

Library GC: 0.484 vs 0.460 for 013. Definitively higher-GC.

## Strong split by eval class
Three eval groups now visible by their GC sensitivity:
- **High-GC favoring**: eval_01,04,08,14 — better with higher GC
  (eval_08 a 0.13 GAIN — largest ever observed)
- **Diversity favoring**: eval_07,10,13 — much worse with high GC
- **Mid-GC robust**: eval_02,05 (mc5 + supplement balance is best)

Eval_01 ★ is mid-GC favoring at the margins; the high-GC push hurts it
because the diversity-favoring components drag it down.

## Conclusion
mc5 base + cCRE supplement (013) sits at a local optimum because mc5's
mean GC (~0.42) leaves room for the high-GC supplement to balance without
overshooting. Pushing the base GC up to 0.46 over-shifts the library
and breaks eval_07/13.

## Implication
Cannot break the 0.5765 eval_01 ceiling by raising GC. Need orthogonal
moves. Next: synthesize a GC-histogram-matched supplement from genomic
windows — tests whether GC distribution shape is the FULL explanation
of the cCRE supplement.
