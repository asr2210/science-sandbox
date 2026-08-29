# 024 — iid mass curvature test (32.5K cCRE 6.5K-each + 7.5K iid + 5K human + 5K chicken)

## Result — iid mass past 5K is SHARPLY harmful
| metric  | 024 | 010 | Δ vs 010 |
|---------|-----|-----|----------|
| eval_01 | 0.7107 | **0.7599** | −0.0492 |
| eval_02 | 0.8029 | **0.8550** | −0.0521 |
| eval_03 | 0.7852 | **0.8413** | −0.0561 |
| eval_04 | 0.7734 | **0.8140** | −0.0406 |
| eval_05 | 0.7107 | **0.7599** | −0.0492 |
| eval_06 | 0.8027 | **0.8550** | −0.0523 |
| eval_07 | 0.7356 | **0.8044** | −0.0688 |
| eval_08 | 0.6708 | **0.7515** | −0.0807 |
| eval_09 | 0.8378 | **0.8872** | −0.0494 |
| eval_10 | 0.7597 | **0.8233** | −0.0636 |
| eval_11 | 0.6978 | **0.7464** | −0.0486 |
| eval_12 | 0.6737 | **0.7244** | −0.0507 |
| eval_13 | 0.7292 | **0.8016** | −0.0724 |
| eval_14 | 0.8028 | **0.8551** | −0.0523 |

Mean 14: **0.7495** vs 010=0.8056 (Δ=−0.0561). Wall: 921s (moderate
impairment).

## Per-seed eval_01
- seed 0: 0.7098
- seed 1: 0.7207
- seed 2: 0.7015

Spread = 0.019 (slightly elevated above 010's 0.012). Consistent
across seeds — not a one-bad-seed artifact.

## Pre-registered scorecard
- "024 ≈ 010 within ±0.005 (linear cancel)": **falsified** (Δ=−0.056).
- "024 > 010 by +0.005-0.015 (NEW BEST)": **falsified** (much worse).
- "024 < 010 by 0.005-0.020 (iid saturated)": **partially confirmed
  in direction, magnitude FAR EXCEEDS prediction** (Δ=−0.056, 3× the
  predicted ceiling).

## Decomposition of 024's −0.056
Using cCRE elasticity from 014 (+5K cCRE costs 0.038, so −2.5K cost
≈ 0.019, assuming linear) and assigning the residual to iid mass:

| component | Δ |
|-----------|------|
| cCRE 35K → 32.5K (preserving balance) | ~−0.019 |
| iid 5K → 7.5K (uniform composition) | **~−0.037** |
| **Sum** | **−0.056** |

So iid going from 5K to 7.5K costs **~−0.037 over 2.5K extra iid =
−0.015/K negative marginal value**. The iid mass axis has a sharp
peak at 5K, with steep negative slope going past it.

## Theory update — iid mass peaks sharply at 5K
**Refined theory (v8).**
> iid mass has a sharp peak at 5K (10% of total library):
>   - Below 5K: each iid element worth ~+0.011 mean per K (scaling
>     from 0 → 5K = +0.056 total, from 012 iid-removal experiment).
>   - At 5K: optimal anchor strength.
>   - Above 5K: each additional iid element worth ~−0.015 mean per K
>     (signal dilution + reduced cCRE attention).
> The peak is sharp because iid contributes via two competing
> mechanisms that crossover at ~5K:
>   (i) Calibration-anchor (saturating, helpful at low mass)
>   (ii) Signal-dilution (linear, harmful at any mass, dominates
>        once anchor saturates)

**Possible mechanism for the dilution side:**
- With 7.5K iid (15% of library), too much training capacity goes to
  "this is random" rather than "what motif is here".
- Iid sequences have low/zero MPRA activity by construction. With
  larger iid mass, the regression target distribution gets pulled
  toward zero, reducing dynamic range for cCRE predictions.
- Model attention budget is finite; more iid = less cCRE attention.

## Joint optima of 010 — remarkable coincidence
010 sits at the joint optimum of MANY axes simultaneously:
- cCRE: 35K (sharp peak, 014/015 elasticity)
- iid: 5K (sharp peak, 024)
- iid composition: uniform 50% GC (asymmetric peak, 021/022/023)
- cCRE class balance: 7K-each (near-flat-bottom optimum, 020)
- Cross-species: chicken at 5K (best species, sharply special, 011/017)
- Cross-species per-species mass: 5K (universal cap, 008/015)
- Cross-species count: saturates at 1 (007/008/009)
- Hard negatives: avoided (016)
- 4 components at 5K each: validated (012)

This is striking — the 010 design was settled by experiment 010 via
empirical comparison to 006 (mouse swap), NOT via gradient ascent
over each axis. The fact that it sits at the joint optimum of ~9
distinct sub-axes is partly luck and partly that the early-loop
intuitions were good.

**Prediction:** unless a fundamentally NEW high-value component exists,
beating 010 by >+0.005 is unlikely from rebalancing within established
axes. New BEST would require finding a new source-type that
contributes >+0.005 net value (after accounting for displaced
component cost).

## What I learned (operational)
1. **Sharp peaks are common.** cCRE mass, iid mass, iid composition,
   cross-species mass — all have sharp single-point optima with steep
   falloff. Small library design changes can have outsized effects.
2. **Component values are NOT additive past the peak.** Above-peak
   mass adds negative marginal value. Linear extrapolation from
   removal-cost (5K iid removed = −0.056) is misleading on the upside.
3. **The 010 baseline is robust.** After 14 follow-up experiments
   probing every known axis, 010 has not been beaten. It's a true
   joint optimum within the space of [cCRE, iid, cross-species,
   human-gen] designs.

## What to try next
The 4-axis design space appears exhausted. Beating 010 requires a
genuinely NEW high-value component. **025: replace human-gen (modest
+0.005 value) with reverse-complemented cCRE** as the 4th 5K
component. RC-cCRE preserves real motifs but in reverse-complement
orientation — tests whether the model is strand-aware enough to
benefit from RC-augmented motif diversity.

Library: 35K cCRE 7K-each + 5K iid + 5K RC-cCRE + 5K chicken = 50K.
Replaces human-gen with RC-cCRE.

Pre-registered:
- 025 > 010 by +0.005-0.015: model is partially strand-aware; RC
  provides new motif views the model can use. **POSSIBLE NEW BEST.**
- 025 ≈ 010 within ±0.010: model handles strand internally (data
  augmentation in prepare.py); RC-cCRE is redundant with the existing
  cCRE component.
- 025 < 010 by 0.005-0.020: RC-cCRE acts like dinuc-shuffled cCRE
  (016) — preserves composition/dinuc but disrupts orientation-
  specific motifs that the model relies on; net harmful.

This is high-information regardless of outcome. Going with 025.

Alternatives considered:
- **025: 4K iid (downside test)**: closes iid mass axis but predicted
  outcome is small (~−0.005); low information.
- **025: replace human-gen with CpG islands**: requires CpG-island
  bed file, likely overlaps PLS heavily.
- **025: replace human-gen with conserved non-coding elements**:
  requires phastCons download.
- **025: replace human-gen with another amniote (turkey)**: predicted
  to be redundant with chicken.
- **025: synthetic motif-rich sequences**: requires JASPAR motifs.

RC-cCRE is the cleanest novel-component test using only existing data.
