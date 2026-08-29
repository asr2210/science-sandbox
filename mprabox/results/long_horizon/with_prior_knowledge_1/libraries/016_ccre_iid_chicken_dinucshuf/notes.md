# 016 — cCRE (35K) + iid (5K) + chicken (5K) + dinuc-shuffled cCRE (5K)

## Result — dinuc-shuffled cCRE is WORSE than empty space
| metric  | 016 | 010 | 014 | Δ vs 010 | Δ vs 014 |
|---------|-----|-----|-----|----------|----------|
| eval_01 | 0.7065 | **0.7599** | 0.7285 | −0.0534 | −0.0220 |
| eval_02 | 0.7976 | **0.8550** | 0.8196 | −0.0574 | −0.0220 |
| eval_03 | 0.7771 | **0.8413** | 0.8020 | −0.0642 | −0.0249 |
| eval_04 | 0.7708 | **0.8140** | 0.7888 | −0.0432 | −0.0180 |
| eval_05 | 0.7066 | **0.7599** | 0.7284 | −0.0533 | −0.0218 |
| eval_06 | 0.7976 | **0.8550** | 0.8198 | −0.0574 | −0.0222 |
| eval_07 | 0.7236 | **0.8044** | 0.7531 | −0.0808 | −0.0295 |
| eval_08 | 0.6631 | **0.7515** | 0.7015 | −0.0884 | −0.0384 |
| eval_09 | 0.8374 | **0.8872** | 0.8579 | −0.0498 | −0.0205 |
| eval_10 | 0.7545 | **0.8233** | 0.7811 | −0.0688 | −0.0266 |
| eval_11 | 0.6941 | **0.7464** | 0.7155 | −0.0523 | −0.0214 |
| eval_12 | 0.6679 | **0.7244** | 0.6903 | −0.0565 | −0.0224 |
| eval_13 | 0.7148 | **0.8016** | 0.7419 | −0.0868 | −0.0271 |
| eval_14 | 0.7978 | **0.8551** | 0.8200 | −0.0573 | −0.0222 |

Mean 14: **0.7435** vs 010=0.8056 (−0.0621) vs 014=0.7677 (−0.0242). Wall: 934 s.

## Per-seed eval_01
- seed 0: 0.6998
- seed 1: 0.6876
- seed 2: 0.7322

Spread = 0.045. Wider than 010 (0.010), comparable to 014 (0.060).

## Pre-registered scorecard
- "016 ≈ 010 (within ±0.005, dinuc substitutes for human-gen)":
  **strongly falsified**.
- "016 between 010 and 014 (dinuc adds something)": falsified.
- "016 ≈ 014 (dinuc adds nothing)": falsified.
- "016 < 014 (dinuc actively confuses)": **confirmed** with magnitude
  −0.024 below 014.

## Disentangling the −0.024 vs 014
014 (40K cCRE + 5K iid + 5K chicken) = 0.7677.
016 (35K cCRE + 5K iid + 5K chicken + 5K dinuc-shuffled cCRE) = 0.7435.

So 016 trades 5K cCRE for 5K dinuc-shuffled cCRE. From the 014 vs 010
analysis, cCRE 35→40K = −0.031 mean, so cCRE 40→35K (the inverse swap)
should give +0.031 mean. Combined with adding 5K dinuc-shuffled cCRE,
the actual change is −0.024. So:

  dinuc-shuffled cCRE 5K contribution ≈ −0.024 − (+0.031) = **−0.055
  mean** at 5K mass.

**Dinuc-shuffled cCRE is sharply NEGATIVE**, not just neutral. Adding
5K of dinuc-shuffled cCRE is like spending the budget AND doing harm
on top.

## Why dinuc-shuffled cCRE actively hurts
Hypothesis: the model sees 5K of "cCRE-statistics-matching" sequences
that are NOT in the activity-prediction ground truth (they're synthetic).
Since the model is a regression head, it learns to predict some
baseline activity for these. But because they preserve cCRE
dinucleotide stats, the model can't easily distinguish them from real
cCRE based on low-order stats — it has to use long-range / motif
features. This "dilutes" the model's representation of real cCRE
features by pushing it to associate cCRE-like dinuc statistics with
NEAR-zero activity (or whatever baseline emerges).

In contrast, IID (uniform random) is so distributionally far from real
DNA that the model can trivially route it to a separate path. Mono-
shuffled (005) was BETWEEN — distinguishable on single-nuc stats but
preserves base composition. The model can learn to use "is this base-
composition-matched-but-locally-random" as a feature. Dinuc-shuffled
goes too far: it removes the feature the model needs to use to
distinguish.

**Hard-negative axis is NOT useful in this regime.** Likely needs
either (a) much smaller mass (<1K) to provide weak calibration
without dilution, or (b) very different shuffling that doesn't match
cCRE-class statistics so closely.

## Theory update — hard-negatives derived from cCRE are anti-helpful
> 5th-axis tested via dinuc-shuffled cCRE: VALUE ≈ −0.055 mean at 5K.
> Strongly negative. Hard-negatives derived from real signal sequences
> by k=2-preserving shuffle dilute the model's representation rather
> than improving it.
>
> Mono-shuffled (005, smaller mass) had smaller negative effect.
> The badness scales with how cCRE-statistic-matched the negative is.
>
> Practical lesson: do not use shuffled sequences as a 5th axis.
> Off-distribution synthetic content (iid uniform) only works because
> it's clearly outside the manifold.

## What I learned (operational)
1. **"Hard negatives are good for ML training" doesn't generalize to
   activity regression on noisy ground truth.** This is regression on
   experimental MPRA-like signals, not classification. Hard negatives
   in regression imply we're forcing the model to commit to a baseline
   prediction for sequences with no real ground truth. Bad.
2. **Three negative results in a row (014, 015, 016) all confirm 010
   sits at a local optimum.** The 4-axis design is fully tuned. Going
   forward, any improvement requires GENUINELY DIFFERENT axes —
   not more of, less of, or substitutes-for the 4 we have.
3. **Cost of testing a "novel" axis can be small if the result is
   strongly negative.** 016 told us something we couldn't have known
   without trying. Even negative results constrain the search well.

## What to try next
**017: test xenopus tropicalis as cross-species (between chicken and
zebrafish on the hump).** The 4-axis design is saturated, so the only
remaining route to a NEW BEST is finding a better single cross-species.
Xenopus (~360 Mya) is between chicken (310) and zebrafish (430) — if
the hump peak is at 360 instead of 310, xenopus > chicken at 5K.

Design 017: 35K cCRE + 5K iid + 5K human + 5K xenopus tropicalis
(xenTro10) = 50K. Direct 010-style design with xenopus replacing
chicken. Tests whether xenopus matches or exceeds chicken at 5K.

Pre-registered:
- 017 > 010 by ≥ +0.005: hump peaks at xenopus distance, NEW BEST.
- 017 ≈ 010 (±0.005): xenopus ≈ chicken, hump is broad with flat peak
  spanning 300-400 Mya.
- 017 between 010 and 011 (loss 0.005-0.010): xenopus is between
  chicken and zebrafish on the hump.
- 017 ≈ 011 or worse: xenopus is no better than zebrafish, hump peaks
  sharply at chicken.

Requires download of xenTro10.2bit (~480 MB). Implementation uses the
same `random_nonhuman_genomic` template as 011's zebrafish.