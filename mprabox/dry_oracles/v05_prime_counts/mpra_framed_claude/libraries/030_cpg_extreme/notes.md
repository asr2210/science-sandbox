# Exp 030 — Extreme CpG enrichment (top 50K of 500K, top 10%)

## Design
Stricter CpG filter than 028. Min CpG-count in selected windows = 5
(median = 6). Library GC=0.539; CpG=0.0395 (vs 028's 0.491 / 0.0265).

## Result
**eval_01 = 0.0485; mean = 0.0449; HepG2 = 0.0522.**

| metric | 013 baseline | 028 top-25% CpG | 030 top-10% CpG |
|--------|--------------|------------------|------------------|
| eval_01 mean | 0.0488 | **0.0524** | 0.0485 |
| K562 eval_01 | 0.0374 | 0.0427 | 0.0425 |
| HepG2 eval_01 | 0.0535 | **0.0610** | 0.0522 |
| SKNSH eval_01 | 0.0529 | 0.0534 | 0.0508 |
| GC | 0.448 | 0.491 | 0.539 |
| CpG | 0.013 | 0.027 | 0.040 |

**Pushing CpG harder OVERSHOOTS.** 030 regresses to 013 baseline.
HepG2 drops most (−0.009 vs 028).

## Interpretation
The CpG axis lift is non-monotone — peaks around top-25% selectivity
(GC ≈ 0.49), inverts at top-10% (GC ≈ 0.54). Mechanism likely:

- 028 (GC 0.49) captures CpG-rich windows near the natural promoter/enhancer
  composition.
- 030 (GC 0.54) pulls in extreme outliers — pure CpG islands, satellite-like
  GC-rich regions — that don't reflect the eval distribution's natural mix.

The training-distribution / eval-distribution match has an optimum at
modest CpG enrichment, not extreme. The same pattern we saw with the
cCRE-fraction sweep (0%, 5%, 20% all ≈ same; 100% PLS hurt).

## Theory update
- **028 (top-25% CpG) is the best library in this 30-experiment run.**
  eval_01 = 0.0524, HepG2 = 0.0610.
- CpG enrichment is a real signal; extreme enrichment overshoots.
- The eval distribution favors **moderate enrichment of regulatory
  features over natural-genomic background**, not pure regulatory
  content or pure random.

## Final notes
End of 30-experiment run. See notebook.md for theory summary and library
ranking.

## Time
57s wall, 26s evaluator.
