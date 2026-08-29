# Exp 024 — 013 design with seed=2 (triplicate)

## Result
**eval_01 = 0.0485; HepG2 = 0.0518.**

## 013 triplicate
| seed | eval_01 | HepG2 |
|------|---------|-------|
| 0 (013) | 0.0493 | 0.0535 |
| 1 (020) | 0.0487 | 0.0534 |
| 2 (024) | 0.0485 | 0.0518 |
| avg | **0.0488** | **0.0529** |
| range | 0.008 | 0.017 |

eval_01 is very stable (±0.001). HepG2 has slightly more variance (±0.008).

## Interpretation
013 is the robust best library, with eval_01 = 0.049 reproducible to
±0.001. Beats 010 random hg38 avg (0.050 from 003/007) by essentially
nothing in eval_01 but slightly more in stability.

## Theory update
The natural-DNA ceiling is firmly 0.049 on eval_01. No design has broken
it across 24 experiments. The 013 mix (80% random hg38 + 20% cCRE) is the
practical recommendation.

## Time
44s wall, 13s evaluator.
