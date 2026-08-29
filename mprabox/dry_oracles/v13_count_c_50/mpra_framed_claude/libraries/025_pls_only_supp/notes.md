# Experiment 025 — PLS-only cCRE supplement

## Result vs 013 (type-balanced cCRE)
| eval | 013 | 025 (PLS only) | Δ |
|------|-----|----------------|---|
| 01 ★ | **0.5765** | 0.5674 | -0.009 |
| 04 | 0.5774 | **0.5873** | +0.010 |
| 07 | **0.6037** | 0.5817 | -0.022 |
| 08 | 0.1730 | **0.2215** | +0.049 |
| 13 | **0.5865** | 0.5626 | -0.024 |

Supp GC: 0.628 (PLS) vs 0.527 (balanced cCRE). Library GC: 0.490 vs 0.460.

## Verdict: same trade-off pattern as all GC pushes
Concentrating on the highest-GC cCRE type (PLS = promoter/CpG island)
shifts the library toward higher GC. Wins eval_08 (+0.05) but loses
eval_07/13 (-0.02 each). Net eval_01 down 0.009.

This is the SAME shape as exp 021 (high-GC base) and exp 019 (GC-filter
supplement): high-GC narrow boosts eval_04/08, hurts eval_07/13.

## Strongest pattern across all libraries
| library | eval_08 | eval_07/13 | eval_01 |
|---------|---------|------------|---------|
| 014 PhastCons (low GC) | -0.003 | 0.62/0.62 | 0.554 |
| 013 type-balanced cCRE | 0.173 | 0.60/0.59 | **0.5765** |
| 025 PLS only | 0.222 | 0.58/0.56 | 0.567 |
| 021 high-GC base | 0.299 | 0.52/0.50 | 0.545 |
| 019 GC-filter [0.5,0.8] | 0.225 | 0.56/0.54 | 0.551 |

There is a clean monotonic trade-off along the GC axis. 013 sits at
the eval_01-maximum point of this trade-off curve.

## Insight: type balance preserves a NATURAL compositional spread
PLS-only narrows the supplement composition (all promoter-like). Type
balance preserves variance. The natural cCRE mix (in 009) and the
type-balanced cCRE mix (013) are both near-optimal because they sample
the FULL natural distribution of cCRE compositions.
