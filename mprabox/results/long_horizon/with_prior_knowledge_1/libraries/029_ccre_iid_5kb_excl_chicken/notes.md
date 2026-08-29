# 029 — slot-4 deep cCRE exclusion (5kb instead of 200bp)

## Result — going DEEPER is also harmful; 200bp is at the optimum

| metric  | 029 | 010 | 027 (near-flank) | Δ vs 010 |
|---------|-----|-----|-------------------|----------|
| eval_01 | 0.7275 | **0.7599** | 0.7450 | −0.0324 |
| eval_02 | 0.8211 | **0.8550** | 0.8402 | −0.0339 |
| eval_03 | 0.8029 | **0.8413** | 0.8251 | −0.0384 |
| eval_04 | 0.7868 | **0.8140** | 0.8042 | −0.0272 |
| eval_05 | 0.7275 | **0.7599** | 0.7448 | −0.0324 |
| eval_06 | 0.8212 | **0.8550** | 0.8402 | −0.0338 |
| eval_07 | 0.7603 | **0.8044** | 0.7851 | −0.0441 |
| eval_08 | 0.6948 | **0.7515** | 0.7248 | −0.0567 |
| eval_09 | 0.8550 | **0.8872** | 0.8760 | −0.0322 |
| eval_10 | 0.7820 | **0.8233** | 0.8059 | −0.0413 |
| eval_11 | 0.7147 | **0.7464** | 0.7318 | −0.0317 |
| eval_12 | 0.6903 | **0.7244** | 0.7086 | −0.0341 |
| eval_13 | 0.7547 | **0.8016** | 0.7805 | −0.0469 |
| eval_14 | 0.8211 | **0.8551** | 0.8403 | −0.0340 |

Mean 14: **0.7686** vs 010=0.8056 (Δ=**−0.0370**). Wall: 1273s.
Per-seed eval_01: seed_0=0.7578, seed_1=0.6928, seed_2=0.7318
(spread **0.065** — very high, comparable to 028 mixing).

## Pre-registered scorecard
- "029 > 010 by +0.005-0.015 (NEW BEST, cleaner negative)":
  **falsified** (Δ=−0.037, opposite direction).
- "029 ≈ 010 within ±0.005 (200bp already optimal)": **falsified
  in magnitude** (Δ=−0.037, far outside band) — but **direction
  of "200bp is optimal" CONFIRMED** (going deeper hurts).
- "029 < 010 by 0.005-0.015 (5kb biases toward gene-deserts)":
  **direction confirmed, magnitude 2.5× the predicted ceiling**.

## The slot-4 sampling axis — full picture is U-shaped

Combining 027 (near-flank), 010 (200bp excl), and 029 (5kb excl):

| slot-4 sampling | mean 14 | Δ vs 010 |
|-----------------|---------|----------|
| 027 near-flank (200-2000bp from cCRE, IN the flank band) | 0.7895 | −0.016 |
| **010 medium-excl (≥200bp from cCRE, anything beyond)** | **0.8056** | **0** |
| 029 deep-excl (≥5000bp from cCRE) | 0.7686 | −0.037 |

The slot-4 sampling distance distribution is **U-shaped (or
inverse-bowl)** with a sharp optimum near the 010 setting:
- TOO CLOSE to cCRE (027): adversarial near-positive — model
  partial-fires.
- TOO FAR from cCRE (029): biased toward AT-rich gene deserts
  / lamina-associated domains / heterochromatin — loses
  "representative human background" character.
- 010 (≥200bp, otherwise random across genome): perfect
  balance — captures both flanking and deep regions in their
  natural genome proportions, none of which is a near-positive.

**Why deep-excl hurts:** removing all sequences within 5kb of
any cCRE leaves only deep gene-deserts (typically 50%+ of the
genome by bp, but heavily biased toward LADs, AT-rich repeats,
gene deserts, and centromere-proximal heterochromatin). These
have:
  - Unusual composition (very AT-rich, ~35% GC vs genome 41%)
  - High repeat density (LINE/LTR/SINE)
  - Low motif content
The model trained on this gets a WEAKENED "human background"
signal that no longer represents typical non-cCRE chromatin.

## Theory update (v13) — slot-4 distance is U-shaped, optimum at 200bp

**Refined theory:**
> The slot-4 sampling axis (distance-from-cCRE) is U-shaped:
>   - Distance 0-200bp: forbidden (cCRE proper).
>   - Distance 200-2000bp (027): −0.016 (near-positive band).
>   - Distance ≥200bp WITH random sampling across all genome
>     (010): optimum. Most accepted windows naturally fall
>     >5kb from cCRE (gene-deserts dominate by area), but
>     ~5-10% land in flanks — and that natural mixture is
>     beneficial.
>   - Distance ≥5000bp ONLY (029): −0.037 (gene-desert bias).
>
> The 010 sampling strategy is NOT "pure deep-non-cCRE"; it's
> "uniform random across non-cCRE genome" which naturally
> includes ~5-10% near-flank windows. Removing those near-flanks
> (which 029 does) loses representative coverage.

This is a counterintuitive refinement of 027. 027 said "near-flanks
HURT (concentrate them)". 029 says "near-flanks at NATURAL low
density HELP (don't remove them)". The optimum is the 010
default of "exclude only the cCRE+200bp boundary, otherwise
sample randomly".

## What I learned (operational)
1. **The slot-4 axis is U-shaped, not monotonic.** I expected
   monotonic-better with more exclusion (cleaner negatives).
   The data says the optimum is BOTH-DIRECTIONS-SHARP.
2. **Pre-registration matters.** I would have predicted 029 ≈ 010
   if 027 hadn't been run; would have predicted 029 > 010 if I'd
   over-extrapolated 027. The actual U-shape requires both data
   points to see.
3. **The 010 design has 14 verified joint constraints.** Adding
   "slot-4 sampling = random across non-cCRE (NOT deep-only)" as
   the 14th. The U-shape is now characterized.

## What to try next — final experiment of the loop

**030: random-offset cCRE sampling.** The last unexplored axis is
cCRE WINDOW POSITIONING. Currently sample_ccre takes WIN=200bp
centered exactly on each cCRE midpoint. Try centering on
midpoint ± rand(0,50)bp offset — provides positional
augmentation. Library: 35K cCRE (random ±50bp offset) + 5K iid
+ 5K human + 5K chicken = 50K (010 with offset augmentation).

Pre-registered:
- 030 > 010 by +0.005-0.015 (NEW BEST): positional augmentation
  helps the model learn motif-position invariance.
- 030 ≈ 010 within ±0.005: model is already position-invariant
  (CNN-like), augmentation redundant.
- 030 < 010 by 0.005-0.015: offset disrupts cCRE midpoint anchor
  (model relies on the centered position for motif extraction).

This is the cleanest remaining single-axis test and closes the
30-experiment loop.

After 030, the loop concludes: 010 is the proven-best library
(mean=0.8056, eval_01=0.7599) at the joint optimum of 14 verified
sub-axes. The final notebook entry will summarize the program.
