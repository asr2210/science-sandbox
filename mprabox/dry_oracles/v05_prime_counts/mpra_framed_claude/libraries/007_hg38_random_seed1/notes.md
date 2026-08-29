# Exp 007 — Variance check: hg38 random windows seed=1

## Design
Identical to Exp 003 (random 200bp windows from chr8/19/22, N-free, forward
strand) but with seed=1 instead of seed=0.

## Result
| metric | seed=0 (003) | seed=1 (007) | Δ |
|--------|--------------|--------------|---|
| eval_01 | 0.0490 | 0.0523 | +0.0033 |
| eval_07 | 0.0320 | 0.0331 | +0.0011 |
| eval_08 | 0.0492 | 0.0473 | -0.0019 |
| eval_13 | 0.0336 | 0.0322 | -0.0014 |
| mean | 0.0457 | 0.0461 | +0.0004 |

## Interpretation
Library-level noise for the same generative process is ~±0.003 on eval_01,
~±0.001 on eval_07/08/13. Cross-library design effects so far span 0.04 to
0.05 (Δ ≈ 0.007), or about 2x the noise. **Design effects are real but
small** — about 2x noise floor.

The dinucleotide experiment (Exp 002) with eval_01 = 0.009 was definitively
worse than baseline (>10x noise).

## Conclusion for strategy
- Reproducibility is good; eval_01 differences ≥ 0.01 are real signal.
- The 0.04–0.05 band is a true plateau for "natural-DNA-distribution"
  libraries. To win meaningfully I need designs that lift eval_01 by
  ≥ 0.02 — clearly above the noise.
- Tiny optimization within this band is wasted effort.

## Time
13s evaluator, 44s wall.
