# 029 — 022-style chimera with 160bp cognate + 20bp random flank each side

## Design
013 class composition (10K rare + 2.5K abundant). Each sequence:
  [20bp random hg38 main-chrom flank]
  [160bp cognate cCRE region centered on cCRE midpoint]
  [20bp random hg38 main-chrom flank]
Random flanks from main-chrom positions >=10kb from any cCRE (same
scaffold pool as 022/023).

## Results (mean over 3 seeds)
- eval_01 = **0.6946** (vs 013 0.7477 = **-0.053**)
- mean across 14 evals = **0.7291** (vs 013 0.7900 = **-0.061**)
- eval_08 = **0.6357** (vs 013 0.7044 = **-0.069**, vs 022 0.7529 = -0.117)

**SURPRISE NEGATIVE.** 029 sits below 013, 022, AND 023 on every axis.

## Per-eval delta vs 013
01:-0.053 02:-0.058 03:-0.062 04:-0.045 05:-0.053 06:-0.058 07:-0.086
08:-0.069 09:-0.051 10:-0.069 11:-0.052 12:-0.054 13:-0.084 14:-0.058

ALL evals lost ~0.045-0.086.

## Per-seed eval_01
seed 0: 0.6986
seed 1: 0.6902
seed 2: 0.6951
SD ≈ **0.004** (extraordinarily tight — same pattern as 024).

## Training time
527s vs typical 1200-2000s. Very fast convergence — model found
something easy.

## Branch outcome
- 029 mean ~0.79 AND eval_08 > 0.73 → minimal-flank chimeric is
  best-of-both → **NO**
- 029 mean ~0.79 AND eval_08 ~0.71 → 20bp flank too small to trigger
  boost → **NO**
- 029 mean < 0.78 → cognate fraction matters even at ~80% → **YES,
  but worse than expected (-0.061, -0.117 on eval_08)**

## What this teaches

**T28 (new — cognate-flank ratio is non-monotone, not a smooth
gradient):** Updated cognate-region table:

| cognate | flank | mean   | eval_08 | exp |
|---------|-------|--------|---------|-----|
| 200bp   |   0bp | 0.7900 | 0.7044  | 013 |
| 160bp   |  20bp | 0.7291 | 0.6357  | 029 |
| 100bp   |  50bp | 0.7873 | 0.7529  | 022 |
|  50bp   |  75bp | 0.7784 | 0.7649  | 023 |
|   0bp   | 100bp | 0.7321 | 0.7841  | 001 |

The 160/20 chimera is WORSE than EITHER endpoint AND worse than the
intermediate chimeras. The function is NOT monotone in flank
fraction; there's a degenerate regime when the flank is too small
to act as a real "scaffold" but big enough to break the cCRE's
boundary. The model converges fast and uniformly across seeds (SD
≈ 0.004) — same fingerprint as 024 (random+cCRE mix, mean=0.7235,
seed SD ≈ 0.0008): the model fits a degenerate easy solution that
generalizes badly.

**T28b (mechanistic conjecture):** Random flanks at 50bp and 75bp
acted as a "context-clearing scaffold" (T22-T24 phenomenology) — they
told the model "ignore me, focus on the central cognate region."
A 20bp flank is too short to read as scaffold, but long enough to
disrupt the natural cCRE width landscape (cCRE widths often
~150-300bp, so a 160bp window is approximately one cCRE-width — but
the 20bp boundary is *close to* the cCRE edge in many cases).
This may create a weak/conflicting signal that the model
overfits to.

**T29 (consequence):** The chimeric-design regime is not "more flank
better" — it has a minimum-effective-flank-fraction. Below that
threshold, the construction is harmful, not neutral.

## Best library so far
**013 cCRE extreme upweight, mean = 0.7900**. Holds.
**022 (mean 0.7873, eval_08 0.7529)** alt-best for eval_08-priority.

## Most informative next experiment (030)
Combining T22/T24 (chimeric eval_08 boost is real and whole-library)
with T27 (narrow cCREs more informative per-instance):

**030 = 022-style chimera (100bp cognate + 50bp random flank each
side) but with cCREs filtered to width <250bp (narrow only).**

This is the only remaining axis I haven't tested that could
plausibly beat 022 on mean while preserving the eval_08 boost.
T27 says narrow cCREs are more informative — 022's chimeric design
gave eval_08 +0.049 — combining them could either:
- (a) yield a new top library (mean ≥ 0.79 + eval_08 ≥ 0.74)
- (b) confirm chimeric x narrow are independent axes (additive ≈ +0.04)
- (c) show interaction (chimeric design uses cCRE EDGE info that
  narrow cCREs don't carry → only marginal lift or even harm)
