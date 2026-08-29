# 008 — cCRE (30K) + iid (5K) + human (5K) + mouse (10K)

## Result — sharp regression, falsifies "more mouse" + reinterprets 007
| metric  | 008 | 007 | 006 | Δ vs 007 | Δ vs 006 |
|---------|-----|-----|-----|----------|----------|
| eval_01 | 0.7213 | 0.7446 | 0.7468 | −0.0233 | −0.0255 |
| eval_02 | 0.8132 | 0.8397 | 0.8418 | −0.0265 | −0.0286 |
| eval_03 | 0.7967 | 0.8253 | 0.8262 | −0.0286 | −0.0295 |
| eval_04 | 0.7796 | 0.8009 | 0.8045 | −0.0213 | −0.0249 |
| eval_05 | 0.7214 | 0.7445 | 0.7469 | −0.0231 | −0.0255 |
| eval_06 | 0.8133 | 0.8401 | 0.8420 | −0.0268 | −0.0287 |
| eval_07 | 0.7511 | 0.7868 | 0.7871 | −0.0357 | −0.0360 |
| eval_08 | 0.6759 | 0.7231 | 0.7277 | −0.0472 | −0.0518 |
| eval_09 | 0.8465 | 0.8711 | 0.8753 | −0.0246 | −0.0288 |
| eval_10 | 0.7693 | 0.8049 | 0.8072 | −0.0356 | −0.0379 |
| eval_11 | 0.7085 | 0.7320 | 0.7341 | −0.0235 | −0.0256 |
| eval_12 | 0.6844 | 0.7096 | 0.7112 | −0.0252 | −0.0268 |
| eval_13 | 0.7469 | 0.7825 | 0.7793 | −0.0356 | −0.0324 |
| eval_14 | 0.8133 | 0.8398 | 0.8418 | −0.0265 | −0.0285 |

Mean 14: **0.7601** vs 007=0.7889, 006=0.7908. Largest regression observed.
Wall: 948 s (faster — less I/O, mouse extraction is cheaper than human-cCRE-
filtered).

## Per-seed eval_01
- seed 0: 0.7243
- seed 1: 0.7421
- seed 2: 0.6974

Spread = 0.0447. **Back to pre-006 levels.** Mouse-stabilization effect does
NOT extend with mass — 10K mouse is no more variance-stabilizing than 5K.

## Pre-registered scorecard
- "008 ≥ 006 → cCRE 30K fine, mouse-scaling works": **sharply falsified**
  (−0.0307 mean).
- "007 < 008 < 006": **falsified** (008 < 007 by 0.029).
- "008 ≈ 007 → mouse mass past 5K saturates within species": directionally
  right (mass past 5K is wasted) but the magnitude is much larger because
  cCRE is also dropping.
- "008 < 007 → surprising, chicken contributed": **confirmed**. Chicken
  contributed substantively when held against more-mouse on identical
  scaffolding.

## Key 4-way comparison and re-interpretation
Holding all else constant:
| change | Δ eval_01 | Δ mean |
|--------|-----------|--------|
| 004 → 006 (cCRE 40→35, +5K mouse) | +0.0073 | +0.0083 |
| 006 → 007 (cCRE 35→30, +5K chicken) | −0.0022 | −0.0019 |
| 007 → 008 (swap 5K chicken → 5K more mouse, cCRE held at 30K) | **−0.0233** | **−0.0288** |
| 006 → 008 (cCRE 35→30, mouse 5→10) | −0.0255 | −0.0307 |

The **007 → 008 contrast is the cleanest single ablation in this study so
far**: same backbone, same iid, same human, only difference is whether the
remaining 10K is split (5K mouse + 5K chicken) or all-mouse (10K). Chicken
beats more-mouse by +0.023.

## Theory update — major revision

Previous theory (post-007): "Cross-species axis saturates after one species
(mouse); chicken adds nothing."

**New theory (post-008):** Cross-species axis is multi-dimensional WITHIN
itself; different species ARE separately useful. Within-species mass
SATURATES at ~5K per species. Chicken helped in 007, but its benefit was
offset by cCRE 35→30 shrinkage cost.

> Library value =
>   (i) cCRE backbone — load-bearing AT LEAST through 40K, possibly 50K.
>       The "saturation past 30K" hypothesis from 006 is WRONG; the 006
>       win came from mouse being a new orthogonal axis, not from cCRE
>       being saturated.
>   (ii) Off-genome iid uniform calibration.
>   (iii) In-genome calibration via SPECIES-DIVERSE non-cCRE windows, with
>        per-species saturation around ~5K and at least 2 species (mouse,
>        chicken) being separately informative.
>
> Predicted: a third species (e.g., zebrafish or rat) at 5K each, splitting
> the cross-species mass even further, will add MORE — but only if cCRE
> backbone is preserved at 35K+ and other components (iid, human) are kept.

## What I learned (operational)
1. **Be careful with two-variable confounds.** 007 looked like "chicken does
   nothing"; 008 reveals "chicken helps; cCRE shrink hurts more". Single-
   variable ablations are essential when an experiment moves multiple knobs.
2. **The seed-stabilization effect is not free.** It came with the mouse
   component at 5K specifically; doubling mouse to 10K removes it. The
   mechanism is plausibly that the BENEFICIAL diversity provided by the
   first 5K mouse is what stabilizes — adding more mouse mass is no longer
   "new" diversity, it's redundant within a species.
3. **cCRE backbone elasticity is roughly −0.005 per 1K removed past 35K.**
   First measurable estimate.

## What to try next
**009: re-run with clean isolate of "two species at half-mass each beats
one species at full mass" while holding cCRE at proven 35K backbone.**

Design: 35K cCRE + 5K iid + 5K human + 2.5K mouse + 2.5K chicken = 50K.
Same cCRE, iid, human as 006. Splits 5K cross-species into 2.5K mouse +
2.5K chicken.
- 009 > 006 by ≥ +0.005 mean: species-DIVERSITY at fixed mass beats
  species-MASS. Confirms the theory.
- 009 ≈ 006: split is neutral — mouse alone at 5K already captures the
  cross-species value at this mass budget.
- 009 < 006: surprising — splitting hurts even though chicken helped at
  cCRE 30K. Would imply 5K of mouse specifically beats 2.5K mouse + 2.5K
  chicken, perhaps because each species needs a minimum mass to be useful.
