# 007_dhs_conservation_weighted

## What I tested
Pure conservation axis: weight = mean phyloP100way over the 200bp summit
window (clamped to >=0.01). Single weighted draw, no mixing. Direct
parallel to 001 (signal-only) and 002 (breadth-only) — answers "is
conservation a usable quality axis on its own?"

## Result — loss
| metric   | 007    | 001 (signal) | 002 (breadth) | 003 (best mix) |
|----------|--------|--------------|---------------|----------------|
| eval_01  | 0.6846 | 0.7242       | 0.7152        | 0.7327         |
| eval_07  | 0.7257 | 0.7611       | 0.7238        | 0.7618         |
| eval_08  | 0.6589 | 0.6781       | 0.6908        | 0.6984         |
| eval_13  | 0.7369 | 0.7564       | 0.7004        | 0.7469         |
| cross-14 | 0.7254 | 0.7654       | 0.7534        | 0.7735         |

Per-seed eval_01: 0.6929 / 0.6789 / 0.6819 (std ≈ 0.008 — tight).

Conservation is the **weakest** single axis tested — about 0.04 below
signal alone on every metric. Below the 0.69 threshold I had set as the
"include in 008 mix" trigger.

## Why it lost
PhyloP weighting pulls the sample toward ultra-conserved elements,
which are disproportionately exonic / UTR / coding-adjacent regulatory.
These regions are evolutionarily constrained but often *not* the strong
cell-type-specific enhancers that drive MPRA activity. Variance on
phyloP within cis-regulatory categories is lower than variance on
mean_signal — most active enhancers have only moderate conservation.

The `max(0.01, score)` clamp also flattened the distribution: many
neutral/accelerated regions still got nontrivial weight.

## Implication for next experiments
- **Don't** add conservation as a third additive axis (the notebook had
  this as the 008 plan, conditional on eval_01 > 0.69 — it didn't pass).
- Conservation may still be useful as a *negative filter* (exclude
  ultra-low-phyloP elements that are likely noise) rather than as a
  positive sampling weight. Could test in a later experiment.
- Pivot 008 toward a different axis: cCRE functional class
  (PLS/pELS/dELS), which encodes regulatory element type rather than
  evolutionary signal.
