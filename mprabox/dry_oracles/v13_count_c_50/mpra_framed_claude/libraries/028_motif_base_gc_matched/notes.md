# Experiment 028 — motif-enriched base with mc5 GC matching

## Design
35k base from cCRE-overlap mc5 windows, GC-subsampled to match plain mc5
random GC distribution. Same composition as 013 base; HIGHER motif density
per window. Plus 15k type-balanced cCRE supplement (013 recipe).

Base GC: 0.431 (matches mc5 random ~0.42). Library GC: 0.460 (matches 013).

## Result vs 013
| eval | 013 | 028 (motif base) | Δ |
|------|-----|-------------------|---|
| 01 ★ | **0.5765** | 0.5717 | -0.005 (noise) |
| 04 | 0.5774 | 0.5675 | -0.010 |
| 07 | 0.6037 | 0.6001 | -0.004 (noise) |
| 08 | 0.1730 | **0.1892** | +0.016 |
| 10 | 0.5087 | 0.5102 | +0.002 (noise) |
| 13 | 0.5865 | 0.5743 | -0.012 |

## Verdict: motif density saturates at random mc5
With composition matched, increasing motif density in the BASE produces:
- Small eval_08 gain (+0.016) — extra motifs in CpG-bearing windows
  give a small compositional boost
- Small losses on eval_04/13 (-0.01)
- Net eval_01 essentially unchanged (-0.005, within noise)

So the motif content in plain random mc5 windows is ALREADY ENOUGH for
the model. Adding more motifs per window doesn't help — the model has
saturated its motif-learning capacity from the base.

## Theory v21 — motif saturation
The +0.110 motif contribution to eval_01 (from exp 026 decomp) is NOT
scalable. The model extracts as much motif information as it can from
35k random mc5 windows; doubling the motif density per window adds ~0.

This may be a CAPACITY limit (model architecture can only learn so
many motifs) or a DIVERSITY limit (cCRE-overlap windows have repeated
motif families, less diverse than truly random genomic).

## What does this mean for the ceiling?
The 0.5765 eval_01 ceiling for the 013 recipe appears to be the
asymptotic best achievable with this library size + composition recipe.
Cannot push it by:
- Adding more motif content (motif saturated)
- Adding more composition variety (interpolation, not super-addition)
- Pushing GC further (trade-off across eval classes)
- Changing source curation (cCRE = GC-hist-matched mc5)
- RC augmentation (neutral)

Remaining unexplored: completely different libraries (motif design,
synthetic sequences with specific TF binding sites, etc.).
