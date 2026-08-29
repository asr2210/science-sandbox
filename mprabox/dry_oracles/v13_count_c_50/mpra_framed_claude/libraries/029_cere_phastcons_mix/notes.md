# Experiment 029 — mild PhastCons tweak inside 013 supplement

## Design
35k mc5 base + 9k type-balanced cCRE + 6k PhastCons (≥30bp). The 15k
supplement is 60% cCRE / 40% PhastCons. Tests if a small conservation
fraction inside the proven cCRE supplement adds value.

cCRE GC: 0.525, PhastCons GC: 0.410, Library GC: 0.445.

## Result vs 013
| eval | 013 | 029 | Δ |
|------|-----|-----|---|
| 01 ★ | **0.5765** | 0.5745 | -0.002 (noise) |
| 04 | **0.5774** | 0.5545 | -0.023 |
| 07 | 0.6037 | **0.6211** | **+0.017** |
| 08 | **0.1730** | 0.1098 | -0.063 |
| 10 | 0.5087 | 0.5136 | +0.005 |
| 13 | 0.5865 | **0.6038** | **+0.017** |

## Interpretation
PhastCons-supplemented library makes a clear trade-off:
- LOW-GC-favoring evals (07, 10, 13): NEW HIGHS — PhastCons is low-GC
  (0.41) and shifts library GC down (0.445 vs 013's 0.460).
- HIGH-GC-favoring evals (04, 08): drop substantially.
- eval_01: essentially unchanged (-0.002, within noise).

The library moved DOWN the GC trade-off axis (same direction as 014
PhastCons-only, but less extreme). eval_01 is balanced across both
axes, so neutral. eval_07 hits a new all-time high of 0.6211.

## Verdict: composition shift, not super-additive
Adding PhastCons to the supplement doesn't add information beyond
composition shift. It moves the library to a different point on the
same GC trade-off surface. eval_01 cannot be improved by sliding along
this axis — it's at the optimum of the trade-off.

## Confirms theory v21
The 0.5765 eval_01 ceiling is the apex of a composition trade-off
surface. Any shift either way (more high-GC via cCRE-only / more
low-GC via PhastCons addition) trades gains on one eval class for
losses on the opposite, with eval_01 unchanged within noise.

## What 029 IS useful for
If the task were eval_07 maximization, 029 would be the best library
yet (0.6211 vs 013's 0.6037, +0.017). Similarly eval_13. This suggests
a library can be *tuned* to a specific eval direction by titrating
composition — useful per-task knowledge.
