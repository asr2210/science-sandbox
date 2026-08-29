# 005_dhs_component_stratified_mix

## What I tested
3,125 sequences per NMF component × 16 components = 50,000. Within each
component, half by mean_signal-weighting and half by numsamples-weighting
(without overlap). Forces equal regulatory-program coverage.

## Result — clear negative
| metric   | 005    | 003 (best) | Δ      |
|----------|--------|------------|--------|
| eval_01  | 0.6946 | 0.7327     | **-0.038** |
| eval_07  | 0.7193 | 0.7618     | -0.043 |
| eval_08  | 0.6489 | 0.6984     | -0.050 |
| eval_13  | 0.7078 | 0.7469     | -0.039 |
| cross-14 | 0.7324 | 0.7735     | **-0.041** |

Per-seed eval_01: 0.6952 / 0.6973 / 0.6913 (very tight, std ~0.003).

## Theory update
**Component-stratification hurts.** Confirms the published baseline
pattern (`dhs_stratified` 0.7055 < `dhs_topic` 0.7232).

**Why it hurts**: forcing 3,125 elements per component drags in many
mid-quality elements from small components (Pulmonary devel., Stromal A)
that would never be sampled by abundance-proportional weighting. The
model needs strong regulatory signal regardless of biological category;
even coverage of program space is a worse trade than concentration on
high-signal elements.

The 16 NMF components are not orthogonal axes of training value — they
are biological labels on a single underlying signal-quality continuum.

## What this updates
**Theory v3 holds with one new line:**
> **Quality-weighted abundance > forced diversity** for library design.
> Letting high-signal/high-breadth elements dominate beats stratification
> across biological categories.

Combined with 004's negative on synthetic, the "diversity / coverage"
hypothesis is taking a beating. The lever isn't more diversity in element
selection — it's **more orthogonal axes of element quality**.

## Implications for next experiment
- Stop testing "force diversity" levers (synthetic, component-stratified).
- Test orthogonal QUALITY axes: conservation (evolutionary functionality),
  cCRE class (functional category — promoter vs enhancer), or
  per-element multi-windows (positional augmentation).
- Conservation is the cleanest test of "generalization-relevant quality"
  because conserved elements encode function preserved across millions of
  years of evolution — by definition transferable across cellular contexts.
