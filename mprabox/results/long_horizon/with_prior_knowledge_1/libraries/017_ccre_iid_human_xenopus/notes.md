# 017 — cCRE (35K) + iid (5K) + human (5K) + xenopus (5K)

## Result — xenopus < zebrafish < chicken; CHICKEN is SHARPLY special
| metric  | 017 | 010 | 011 (zfish) | 006 (mouse) | Δ vs 010 |
|---------|-----|-----|------|------|----------|
| eval_01 | 0.7460 | **0.7599** | 0.7543 | 0.7468 | −0.0139 |
| eval_02 | 0.8404 | **0.8550** | 0.8491 | 0.8418 | −0.0146 |
| eval_03 | 0.8248 | **0.8413** | 0.8357 | 0.8262 | −0.0165 |
| eval_04 | 0.8043 | **0.8140** | 0.8098 | 0.8045 | −0.0097 |
| eval_05 | 0.7459 | **0.7599** | 0.7542 | 0.7469 | −0.0140 |
| eval_06 | 0.8405 | **0.8550** | 0.8492 | 0.8420 | −0.0145 |
| eval_07 | 0.7848 | **0.8044** | 0.7954 | 0.7871 | −0.0196 |
| eval_08 | 0.7265 | **0.7515** | 0.7405 | 0.7277 | −0.0250 |
| eval_09 | 0.8747 | **0.8872** | 0.8810 | 0.8753 | −0.0125 |
| eval_10 | 0.8047 | **0.8233** | 0.8162 | 0.8072 | −0.0186 |
| eval_11 | 0.7329 | **0.7464** | 0.7406 | 0.7341 | −0.0135 |
| eval_12 | 0.7087 | **0.7244** | 0.7191 | 0.7112 | −0.0157 |
| eval_13 | 0.7793 | **0.8016** | 0.7921 | 0.7793 | −0.0223 |
| eval_14 | 0.8406 | **0.8551** | 0.8494 | 0.8418 | −0.0145 |

Mean 14: **0.7896** vs 010=0.8056 (−0.0160) vs 011=0.7990 (−0.0094)
vs 006=0.7908 (−0.0012). Wall: 1297 s.

## Per-seed eval_01
- seed 0: 0.7333
- seed 1: 0.7617
- seed 2: 0.7429

Spread 0.028, comparable to 011's 0.018.

## Pre-registered scorecard
- "017 > 010 by ≥ +0.005 (hump peaks at xenopus, NEW BEST)": falsified.
- "017 ≈ 010 (broad hump)": falsified.
- "017 between 010 and 011 (loss 0.005-0.010)": **partially confirmed**
  on direction but magnitude (Δ −0.016) overshoots — 017 actually
  BELOW 011 (Δ vs 011 = −0.009).
- "017 ≈ 011 or worse (chicken sharply special)": **confirmed**.

## Cross-species hump map RE-INTERPRETED
| species | divergence | mean lift vs 4-axis baseline |
|---------|-----------|------------------------------|
| 5K mouse (006) | 80 Mya | 0.7908 |
| 5K chicken (010) | 310 Mya | **0.8056** ← peak |
| 5K xenopus (017) | 360 Mya | 0.7896 |
| 5K zebrafish (011) | 430 Mya | 0.7990 |

The "hump-shape over evolutionary distance" theory is **falsified by
017**: xenopus (360 Mya, between chicken and zebrafish) is BELOW both
neighbors and even below mouse. The cross-species value function is
NOT smooth in evolutionary distance.

What does match the data?

| species | genome size | gene density | mean |
|---------|-------------|--------------|------|
| chicken (galGal6) | 1.05 Gb | high | **0.8056** |
| zebrafish (danRer11) | 1.35 Gb | medium | 0.7990 |
| mouse (mm10) | 2.61 Gb | medium-high | 0.7908 |
| xenopus (xenTro10) | 1.45 Gb | medium-low | 0.7896 |

**Genome size doesn't fully predict either** — xenopus (1.45 Gb) is
similar to zebrafish (1.35 Gb) but performs much worse (~0.01 below).
Chicken is best AND smallest, but the ranking past chicken doesn't
follow size.

**New theory candidate (post-017): "Aves regulatory grammar share with
human" is the actual signal.** Chicken-human share more recent
regulatory machinery (amniote regulatory grammar conservation) per Mya
than xenopus-human (non-amniote tetrapod). Mouse-human share more
recent grammar but the MOUSE genome is too LARGE/repetitive — random
samples mostly hit non-regulatory mass. Zebrafish has unique teleost
regulatory grammar but still works at ~0.799 because of small-genome
+ functional regulatory density. Xenopus loses on BOTH axes: amphibian
regulatory grammar diverged from human, AND the genome is medium-
sized so random samples are dominated by non-regulatory mass.

This is more complex and harder to test cleanly. The simplest summary:
**chicken is unusually good at this 5K cap; no other species we have
matches it.**

## Theory state — chicken is sharply optimal cross-species at 5K
> Cross-species axis: 5K mass cap is universal (per 008/015), and
> CHICKEN at 5K is the unique optimum among tested species.
> Mechanism likely combines small genome size (high gene density →
> high regulatory signal in random samples) with amniote regulatory
> grammar share (closer to human than amphibian or teleost).
>
> The "evolutionary distance hump" theory from 011 is too simple.
> The actual function depends on (genome size × regulatory grammar
> conservation × per-Mb gene density).

## What I learned (operational)
1. **Three data points fit a curve; four data points test the curve.**
   The 011 hump theory was based on three species (mouse/chicken/
   zebrafish). Adding xenopus broke it. THREE points minimum to fit;
   the fourth is the real test.
2. **Small-genome amniotes might be the special class for cross-species
   axis.** Worth testing OTHER small-genome amniotes (turkey, duck,
   melopsittacus) IF we want to push this axis further. None
   downloadable in current env without significant effort.
3. **The "genome size matters more than evolutionary distance" theory
   is consistent with the data but UNDER-DETERMINED.** Need a small
   non-amniote tetrapod or a large amniote to disentangle.

## What to try next
**018: cCRE class re-balancing.** We've fully tuned the 4-axis MASS
allocation; now test SUB-AXIS structure. Currently cCRE samples 7K
each from 5 classes (PLS, pELS, dELS, CTCF-only, DNase-H3K4me3).
Test whether dropping the "structural" classes (CTCF-only, DNase-
H3K4me3) and redistributing mass to "functional" classes (PLS, pELS,
dELS) improves activity prediction.

Design: 12K PLS + 12K pELS + 11K dELS + 5K iid + 5K human + 5K
chicken = 50K. Drops CTCF-only and DNase-H3K4me3 entirely.

Pre-registered:
- 018 > 010 by ≥ +0.005: structural classes added noise; functional
  classes more informative per element. NEW BEST.
- 018 ≈ 010: class balance doesn't matter much; classes contribute
  roughly equally per element.
- 018 < 010 by 0.005-0.015: structural classes contribute meaningful
  context signal; dropping them hurts mildly.
- 018 < 010 by > 0.015: structural classes are critical anchors;
  PLS+pELS+dELS-only library loses chromatin context model.

Why this is high-information: the cCRE backbone (35K) is the largest
axis in the library. We've never tested its INTERNAL composition. Two
possibilities — class-balance matters (must include all 5) or doesn't
(any-functional-cCRE-mix works) — and both have implications for
future axis design.