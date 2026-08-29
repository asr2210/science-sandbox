# Experiment 019 — GC-filtered genomic supplement

## Design
35k mc5 + 15k random windows from mc5 chroms filtered to GC ∈ [0.50, 0.80].
Supp GC: mean 0.558 (matches cCRE), std 0.053 (NARROWER than cCRE ~0.10).

## Result vs cCRE / shuffled-cCRE
| eval | 013 (cCRE) | 017 (shuf cCRE) | 019 (GC-filter) | 019 vs 013 |
|------|------------|------------------|-----------------|------------|
| 01 ★ | **0.5765** | 0.5761 | 0.5507 | -0.026 |
| 04 | 0.5774 | 0.5766 | 0.5735 | -0.004 |
| 07 | 0.6037 | 0.6024 | 0.5603 | **-0.043** |
| 08 | 0.1730 | 0.1884 | **0.2254** | **+0.052** |
| 10 | 0.5087 | 0.5076 | 0.4752 | -0.034 |
| 13 | 0.5865 | 0.5852 | 0.5431 | -0.043 |

## Verdict: best eval_08 yet, but distribution narrowness hurts diversity
The GC-filter precisely matches cCRE mean GC (0.558 vs 0.55) but with
a much narrower std (0.053 vs ~0.10). Eval_08 — the most composition-
driven eval — *loves* this and hits its highest score in the series.
Eval_07/13 (diversity-rewarding evals) crash.

## Refines theory v13
The "composition recipe" splits into two axes:
- **High mean GC tail** → eval_08 gain (universal compositional signal)
- **Wide distribution / multimodality** → eval_07/13 gain (diversity for
  grammar-aware evals)

cCREs are good at BOTH (their wide multi-type distribution naturally
covers both axes). Pure GC-filter is great at one but bad at the other.
A composite supplement may stack both gains.

## Implications
The 0.5765 eval_01 ceiling of 013 is not a hard floor on composition;
it's the best single-source supplement. A *composite* supplement that
combines a broad source (shuffled cCRE) with a narrow high-GC source
(GC-filter) might exceed it.
