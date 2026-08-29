# 009 — cCRE (35K) + iid (5K) + human (5K) + mouse (2.5K) + chicken (2.5K)

## Result — sharp regression vs 006, falsifies symmetric-split theory
| metric  | 009 | 007 | 006 | Δ vs 006 |
|---------|-----|-----|-----|----------|
| eval_01 | 0.7289 | 0.7446 | **0.7468** | −0.0179 |
| eval_02 | 0.8214 | 0.8397 | **0.8418** | −0.0204 |
| eval_03 | 0.8035 | 0.8253 | **0.8262** | −0.0227 |
| eval_04 | 0.7881 | 0.8009 | **0.8045** | −0.0164 |
| eval_05 | 0.7289 | 0.7445 | **0.7469** | −0.0180 |
| eval_06 | 0.8216 | 0.8401 | **0.8420** | −0.0204 |
| eval_07 | 0.7608 | 0.7868 | **0.7871** | −0.0263 |
| eval_08 | 0.6899 | 0.7231 | **0.7277** | −0.0378 |
| eval_09 | 0.8565 | 0.8711 | **0.8753** | −0.0188 |
| eval_10 | 0.7800 | 0.8049 | **0.8072** | −0.0272 |
| eval_11 | 0.7161 | 0.7320 | **0.7341** | −0.0180 |
| eval_12 | 0.6910 | 0.7096 | **0.7112** | −0.0202 |
| eval_13 | 0.7558 | 0.7825 | **0.7793** | −0.0235 |
| eval_14 | 0.8216 | 0.8398 | **0.8418** | −0.0202 |

Mean 14: **0.7689** vs 006=0.7908 (−0.0219). Loses on every eval. Wall: 1282 s.

## Per-seed eval_01
- seed 0: 0.7605
- seed 1: 0.6940
- seed 2: 0.7323

Spread = 0.0665 — back to pre-006 levels. The seed-stabilization effect
collapses at sub-5K cross-species per species.

## Pre-registered scorecard
- "009 > 006 (diversity at fixed mass beats single-species)": **falsified**.
- "009 ≈ 006 (within 0.003)": **falsified**.
- "009 < 006 by 0.003–0.010": **falsified** (loss is much larger).
- "009 < 006 by > 0.010 (per-species mass minimum is ≥ 2.5K)":
  **confirmed strongly** (−0.022 mean).

## Theory update — per-species mass threshold

Cross-species axis is real and per-species saturating at ~5K — we already
knew that. The new finding from 009: the axis ALSO has a per-species
**minimum** above 2.5K. Below that mass, the species component contributes
~zero (and the lost mass that gave it room is wasted).

Combined picture from 006 / 007 / 008 / 009:
| design (cCRE / iid / hum / mouse / chicken) | mean 14 | Δ vs 006 |
|---------------------------------------------|---------|----------|
| 35 / 5 / 5 / 5 / 0  (006, ref)              | 0.7908  | 0       |
| 30 / 5 / 5 / 5 / 5  (007)                   | 0.7889  | −0.0019 |
| 30 / 5 / 5 / 10 / 0 (008)                   | 0.7601  | −0.0307 |
| 35 / 5 / 5 / 2.5 / 2.5 (009)                | 0.7689  | −0.0219 |

Implications:
1. **Per-species useful mass ≈ 5K.** Below it (009: 2.5K each), nothing
   useful learned. Above it (008: 10K mouse), no marginal benefit.
2. **Cross-species value is per-species, not per-axis-mass.** At 5K each,
   adding chicken to 5K mouse (007) provides ~+0.024 cross-species value,
   only just offset by the cCRE shrinkage cost. But splitting that 5K
   chicken into 2.5K (009) collapses chicken's contribution to zero AND
   loses 2.5K of mouse below its threshold.
3. **The cross-species axis needs both critical mass per species AND
   sufficient species count.** It is NOT continuous with mass — there is a
   step function around 5K per species.

## Refined working theory
> Library value =
>   (i) cCRE backbone, load-bearing past 30K (slope ≈ −0.005 mean per −1K
>       past 35K).
>   (ii) Off-genome iid uniform — small but nonzero, captured at 5K.
>   (iii) In-genome human non-cCRE — small but nonzero, captured at 5K.
>   (iv) Per-species cross-species genomic — STEP-FUNCTION value: 0 below
>        ~5K mass per species, ≈ +0.0075 mean at 5K per species, 0 marginal
>        past 5K. Multiple species stack approximately additively at 5K each.
>
> The theoretical implication: the maximum-value 50K library has cCRE backbone
> as large as we can fit, plus exactly 5K of each diverse axis-source. If
> we can't fit more than 5K of each at the 50K cap, we're already near the
> theoretical optimum at 35K cCRE + 5K each of three other axes.

## What I learned (operational)
1. **Don't assume "more diversity at the same mass is free".** Splitting a
   working component into smaller pieces below its activation threshold
   destroys the value of both pieces.
2. **Step-function value functions are real.** Continuous theories ("more
   diverse → more value") fail at low per-species mass. Future tests
   should always include a control at the 5K per-source step.

## What to try next
**010: clean alternative single-species test.** 35K cCRE + 5K iid + 5K
human + 5K chicken (no mouse). Tests whether 006's win was about mouse
specifically or about ANY 5K of cross-species.
- 010 ≈ 006: cross-species sources are interchangeable at 5K — pick any.
- 010 < 006 by 0.005–0.015: mouse > chicken at this mass; mammalian
  proximity matters.
- 010 > 006: chicken > mouse; greater evolutionary distance creates more
  orthogonal calibration. Surprising; would suggest a "the more distant,
  the better" gradient.
- 010 < 006 by > 0.015: chicken alone is barely useful — its 007
  contribution was synergistic with mouse, not substitutive.

This experiment is symmetric to 006 — same backbone, same iid + human,
same total mass, only the species identity changes. Cleanest single-
variable comparison we can run for the cross-species axis.
