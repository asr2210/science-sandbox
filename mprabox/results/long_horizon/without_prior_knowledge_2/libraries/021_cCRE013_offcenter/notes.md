# 021 — cCRE 013 off-center extraction

## Design
Same class counts as 013 (10K each PLS, CA-CTCF, CA-TF, CA-H3K4me3
+ 2.5K each pELS, dELS, CA, TF), same cCRE pool, but each 200bp
window is shifted by uniform random [-50, +50] bp relative to the
cCRE midpoint. The cCRE midpoint lands at a random position within
the window's central +-50bp.

## Results (mean over 3 seeds)
- eval_01 = **0.7240** (vs 013 0.7477 = **−0.024**)
- mean across 14 evals = **0.7617** (vs 013 0.7900 = **−0.028**)

## Per-eval delta vs 013
01:−0.024 02:−0.026 03:−0.028 04:−0.021 05:−0.024 06:−0.026 07:−0.039
08:−0.044 09:−0.022 10:−0.035 11:−0.023 12:−0.025 13:−0.036 14:−0.026

**Loses on ALL 14 evals** by 0.021-0.044. Average −0.028.
Substantially smaller than 020's −0.058 (no-flank) — positional
prior matters less than flank content.

## Per-seed eval_01
seed 0: 0.7290  (909s training)
seed 1: 0.6929  (535s training)
seed 2: 0.7502  (909s training)

SD ≈ 0.024 (3x 013's 0.008). Same training-time-vs-accuracy pattern
as 020 — when the seed lands on a longer training trajectory, it
hits higher accuracy. Likely the offset-jittered libraries shift the
loss landscape such that early-stopping fires inconsistently.

## Branching outcome
Pre-experiment branches:
- 021 > 013 → off-center forces position-invariant features (no)
- 021 ≈ 013 → model already position-invariant (no)
- 021 < 013 → centered prior is exploited (yes, mildly)

Result: **021 < 013 by 0.028**. The model exploits the centered-cCRE
inductive prior; positional jitter is mildly dilutive.

## What this updates in the theory

**T18 (new — positional prior matters but isn't critical):** The
model is not fully position-invariant. Removing the centered-cCRE
prior costs ~0.028 mean correlation. This is half the cost of removing
the flank itself (T17, ~0.058) but real. The first conv layer +
max-pool gives some position-equivariance, but the dense head learns
position-aware features that get disrupted by jitter.

**T17 (consistent):** Flank still matters more (−0.058) than
positional prior (−0.028). Both effects are additive in nature
(removing one doesn't make the other free), suggesting they are
distinct mechanisms.

**T8 (further refined):** The 013 "best library" is best because of:
1. Functional class specificity (T13): ~0.018 over 006 stratified
2. Rare-class upweighting (T8): ~0.013 over 006
3. Cognate flank context (T17): ~0.058
4. Centered positional prior (T18): ~0.028
Different ablations reveal that flank+position contribute MORE than
the upweighting principle. The recipe is multiplicative-additive.

## Best library so far
**013 cCRE extreme upweight, mean ≈ 0.7900**. Holds.

## Process note
spark06 hung on multi-seed run; first attempted multi-seed completed
spark01 (eval_01=0.7290) and spark03 (eval_01=0.7502) but failed on
spark06 → sys.exit(1) and no result.json. Re-ran all 3 seeds via
single-seed local mode. 1: spark01 vs local-seed-0 results match
exactly (0.7290), confirming model_seed=0 hardcoded determinism.

## Most informative next experiment (022)
T17 says flank matters but doesn't isolate the mechanism. Two
candidate explanations:
(a) cognate flank carries regulatory signal (co-binding TFs,
    nucleosome positioning, cell-type-specific context)
(b) flank is scaffold — any DNA there helps the convnet's
    receptive field; specific content doesn't matter

Test by *replacing* the outer 50bp on each side with random hg38
windows (sampled from non-cCRE main-chrom positions). Middle 100bp =
cognate cCRE region; outer 100bp = random-genome flank.
- 022 ≈ 013 → flank is scaffold (b); cCRE element + arbitrary
  flanking context is sufficient
- 022 ≈ 020 → cognate flank specifically matters (a); the random
  flank degrades performance to no-flank levels
- 022 between → both mechanisms contribute partially
