# 028 — MIXED iid composition (35K cCRE + 2.5K uniform + 2.5K hg38-matched + 5K human + 5K chicken)

## Result — mixing iid is SUB-LINEAR, worse than EITHER pure composition

| metric  | 028 | 010 (uniform) | 021 (hg38-matched) | Δ vs 010 |
|---------|-----|---------------|---------------------|----------|
| eval_01 | 0.7311 | **0.7599** | 0.7439 | −0.0288 |
| eval_02 | 0.8241 | **0.8550** | 0.8383 | −0.0309 |
| eval_03 | 0.8075 | **0.8413** | 0.8236 | −0.0338 |
| eval_04 | 0.7932 | **0.8140** | 0.8000 | −0.0208 |
| eval_05 | 0.7310 | **0.7599** | 0.7439 | −0.0289 |
| eval_06 | 0.8244 | **0.8550** | 0.8384 | −0.0306 |
| eval_07 | 0.7668 | **0.8044** | 0.7835 | −0.0376 |
| eval_08 | 0.6956 | **0.7515** | 0.7187 | −0.0559 |
| eval_09 | 0.8617 | **0.8872** | 0.8707 | −0.0255 |
| eval_10 | 0.7858 | **0.8233** | 0.8021 | −0.0375 |
| eval_11 | 0.7184 | **0.7464** | 0.7308 | −0.0280 |
| eval_12 | 0.6944 | **0.7244** | 0.7089 | −0.0300 |
| eval_13 | 0.7614 | **0.8016** | 0.7788 | −0.0402 |
| eval_14 | 0.8243 | **0.8551** | 0.8383 | −0.0308 |

Mean 14: **0.7728** vs 010=0.8056 (Δ=**−0.0328**) vs 021=0.7871
(Δ=−0.0143). Wall: 1267s. Per-seed eval_01: seed_0=0.7596,
seed_1=0.7409, seed_2=0.6928 (spread **0.067** — highest of any
experiment, even above 026's 0.055).

## Pre-registered scorecard
- "028 > 010 by +0.005-0.015 (NEW BEST, mechanisms additive)":
  **falsified** (Δ=−0.033, opposite direction).
- "028 ≈ 010 within ±0.005 (linear cancel)": **falsified**
  (Δ=−0.033, 6× outside band).
- "028 < 010 by 0.005-0.020 (mechanisms dilute)": **direction
  confirmed, magnitude 1.7× the predicted ceiling**.

**The naïve linear prediction was −0.009** (mean of 010 and 021).
Actual −0.033 → mixing is **3.7× worse than linear**. The two iid
compositions don't add; they interfere.

## Theory update (v12) — iid composition COHERENCE matters; anchors need 5K of consistent type

**Refined theory:**
> The iid component acts as a "calibration anchor" that requires
> COHERENT composition mass, not split mass. The 024 finding (iid
> mass peaks sharply at 5K, falling on both sides) reflects a
> single coherent-anchor mechanism. Splitting iid into two
> compositions effectively gives the model 2.5K of EACH anchor
> type, both of which are sub-effective alone.
>
> Below 5K of consistent composition: the iid anchor cannot
> establish a clear "this is NOT real DNA" signal. The model
> sees "some sequences are uniform random + some are hg38-mononuc-
> matched + a lot of cCRE" and treats it as noise rather than
> two coherent calibration streams.
>
> The 010 design's 5K uniform iid is at the joint optimum of
> (mass, composition coherence). Splitting either dimension
> degrades the anchor.

**Operational corollary:** the iid axis is **fully closed**.
- Mass: 5K is the unique peak (024).
- Composition: uniform 50% GC is uniquely optimal (021/022/023).
- Coherence: must be 5K of a SINGLE composition (028).

## Why is the per-seed spread so large?
seed_2 = 0.6928 is the worst single-seed result of any non-broken
experiment (worse than 026's seed_0 = 0.7033, 023's seed_1 = 0.7359).
This suggests that the iid mixing creates an unstable anchor — small
random differences between the 2.5K-uniform and 2.5K-hg38-matched
populations across seeds can produce very different model behavior.

The seed_2 catastrophe is consistent with the "anchor coherence"
theory: when no single iid composition reaches 5K, the model's
calibration depends sensitively on the random sampling of which
2.5K hg38-matched sequences are drawn.

## What I learned (operational)
1. **Mechanism mixing is dangerous.** I expected at-best additive,
   at-worst dilution. Got SUB-linear interference. Theory v12
   adds "coherence" as a third iid axis dimension.
2. **The 010 design now has 13 verified joint constraints.**
   Adding "iid composition coherence" to the list. Beating 010 is
   essentially closed via single-axis OR mechanism-mixing.
3. **Per-seed spread >0.05 is now a clear "broken library"
   signal.** 016 (broken), 022 (broken), 026 (platypus-induced),
   028 (mixing-induced) all show spreads > 0.05. Stable
   libraries (010, 011, 023) have spreads ≤ 0.03.

## What to try next

The remaining unexplored axes are second-order. The two cleanest
remaining tests:

**029: tighter slot-4 cCRE exclusion (5kb instead of 200bp).**
010 excludes human-gen within 200bp of any cCRE. The 027 finding
(near-flank within 200-2000bp is harmful) suggests EVEN MORE
exclusion might help — sample human-gen only from windows ≥5kb
from any cCRE (deeper gene-deserts only). Tests whether 010's 200bp
exclusion is sufficient or if cleaner-negative-anchor improves
slot 4.

**030: random offset within cCRE (±50bp).** Currently sample_ccre
extracts WIN=200bp centered on each cCRE midpoint. Could sample
WIN=200bp at midpoint ± rand(0,50)bp offset — provides positional
augmentation. Tests whether the model is positionally rigid or
benefits from offset variation.

Going with **029 first** because it directly extends the 027/025/016
"near-positive" ladder and probes the LIMIT of the deep-non-cCRE
strategy. If 5kb-exclusion > 200bp-exclusion, NEW BEST possible.
If equal, 010's 200bp is at the optimum. If worse, 5kb is too
restrictive (sample bias toward gene deserts).

Pre-registered:
- 029 > 010 by +0.005-0.015 (NEW BEST): cleaner negative anchor.
- 029 ≈ 010 within ±0.005: 200bp exclusion already optimal.
- 029 < 010 by 0.005-0.015: 5kb exclusion biases toward AT-rich
  gene-desert sequences that don't capture the "human background"
  well.

030 (random offset cCRE) deferred to follow 029.
