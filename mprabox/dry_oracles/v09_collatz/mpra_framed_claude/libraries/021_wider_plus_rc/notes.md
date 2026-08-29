# 021_wider_plus_rc

## Design
5K cCREs × 5 tiles (offsets ±400bp) + each tile's RC = 50K.
Stacks two helpful interventions: wider offsets (020 lift) +
RC augmentation (012 lift).

## Result vs 020 / 012 / 014
                eval_01  K562    HepG2   SKNSH   eval_07
014 narrow:     0.3181   0.144   0.188   0.623   0.337
012 narrow+RC:  0.3195   0.144   0.191   0.624   0.338
020 wider:      0.3216   0.144   0.200   0.621   0.338
021 wider+RC:   0.3222   0.145   0.200   0.622   0.340 ← new high

eval_01 +0.0006 over 020 (marginal). eval_07 new high (0.340).
HepG2 stays at 0.20.

## Interpretation
The lift from RC on top of wider tiles is essentially zero. The two
interventions are NEARLY REDUNDANT — the model already gets enough
strand-invariance training from the wider context distribution, so
adding explicit RC pairs is just a small denoiser.

The wider-offset lever (020) carries most of the lift; RC by itself
(012) carries a smaller fraction.

## Theory T14 (refined)
The "skill axes" that lift the plateau:
1. **CONTEXT BREADTH** (wider tiles): teaches positional invariance
   + context-only inference. Biggest single lever found (+0.004).
2. **STRAND INVARIANCE** (RC): tiny additional lift on top of
   narrow tiling (+0.002), diminishes to nothing on top of wider
   tiles.

These are universal regulatory priors. Stacking them is allowable
but with diminishing returns once the model's effective capacity
on universal-prior axes is saturated.

## What else might help?
- **Even wider tiles (±800)**: tests whether context lift is
  monotonic or peaks somewhere. If wider helps, the model is
  capacity-bound on context-richness.
- **Wider + MORE regions**: 10K cCREs × 5 wider tiles = 50K.
  Tests whether saturation point moves up with wider context.
  (Possible interaction: wider tiles raise effective per-region
  information, so fewer regions needed for saturation; OR more
  context-rich examples needed, so saturation point goes UP.)
- **Wider + class-balanced**: 1K each of 5 cCRE classes × 10 wider
  tiles = 50K. Tests whether class+context combine.

## Next
Experiment 022: EVEN WIDER tiles (±800bp). 5K cCREs × 10 tiles
with offsets in [-800, 800]. The 200bp window can land up to 1kb
from the cCRE midpoint — many tiles will miss the cCRE entirely
and rely on flanking context alone.

Generalization justification: the broader the context exposure,
the more the model learns general "what does the genome look like
near regulatory elements" grammar — universal across cell types.
If wider-still helps, context is the lever to push.

Prediction: If 020's lift comes from rich-context exposure, ±800
should lift further. If 020 already exhausted that axis, ±800
matches or slightly drops (more flanking tiles miss the core
element entirely and add noise).
