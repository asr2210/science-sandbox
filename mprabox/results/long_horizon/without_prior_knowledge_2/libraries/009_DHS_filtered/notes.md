# 009 — DHS Index filtered by signal strength

## Design
DHS Index filtered to **mean_signal ≥ q75 (0.762) AND numsamples ≥ 5**
= 681,721 elements (19% of full DHS Index). Uniform sample 50K, 200bp
centered on summit. Sister to 008 (full DHS uniform) and 002 (cCRE
uniform). Tests whether peak-quality filtering closes the cCRE-DHS gap.

## Results (mean over 3 seeds)
- eval_01 = **0.7106** (vs 008 0.6914 = +0.019; vs 002 0.7263 = −0.016)
- mean across 14 evals ≈ **0.7500** (vs 008 0.7297 = +0.020; vs 002
  0.7665 = −0.017)

## Per-eval delta vs 008 (full DHS uniform)
01:+0.019 02:+0.021 03:+0.016 04:+0.033 05:+0.019 06:+0.021 07:+0.001
08:+0.043 09:+0.038 10:+0.034 11:+0.018 12:+0.014 13:−0.014 14:+0.022

Filtering helps 13/14 evals. Strongest gain on eval_08 (+0.043) and
eval_09 (+0.038). Weak/no effect on eval_07 and eval_13.

## Per-eval delta vs 002 (cCRE uniform)
01:−0.016 02:−0.017 03:−0.023 04:+0.002 05:−0.016 06:−0.018 07:−0.036
08:−0.007 09:+0.004 10:−0.006 11:−0.016 12:−0.019 13:−0.047 14:−0.017

Filtered DHS still loses to cCRE on 12/14 evals, but the gap shrank
from −0.037 (008) to −0.017 (009). On eval_04, eval_08, eval_09,
filtered DHS is now competitive with or beats cCRE uniform.

## Across-seed
eval_01: 0.6862 / 0.7546 / 0.6909 → SD ≈ **0.038**, HIGHER than
008's 0.012. Filtering reduces the pool size (681K vs 3.59M) and
increases seed-to-seed variability. Seed 1 is an outlier (0.7546).

## Branching outcome
Pre-experiment, three outcomes were defined:
- 009 ≈ 002 → filtering recovers cCRE performance (curation = noise)
- 009 between 008 and 002 → curation helps, class-typing adds extra
- 009 ≈ 008 → curation doesn't help; class-typing is the active variable

Result: **009 is between 008 and 002, closer to 002.** Outcome 2.
Peak-quality filtering recovers ~55% of the gap; the remaining ~45%
must be due to something the cCRE pipeline does beyond peak strength
(class-typing, multi-mark filtering with H3K4me3/H3K27ac/CTCF, or
distinct genomic-context selection).

## What this updates in T7
**T7 (refined):** Annotation curation has at least two separable axes:
(a) **peak quality** — filtering weak/rare DNase calls accounts for
~55% of the cCRE-DHS gap. (b) **regulatory typing** — the cCRE
class-assignment + multi-mark filtering accounts for ~45% of the gap
beyond what peak filtering provides.

This means: future experiments can use **filtered DHS as a "DHS-only"
baseline** that controls for peak quality, isolating the regulatory-
typing contribution.

## Best library so far
006 stratified, mean ≈ 0.7754. Unchanged.

## Most informative next experiment (010)
**Class-stratify within cCRE PLUS upweight rare TFs.** 006 stratified
by cCRE class (8 classes), but didn't control for *which transcription
factors* are present in the dELS pool (the largest class). dELS is
heterogeneous — some are AP-1-driven, some FOX-driven, etc. 

Plan: within each cCRE class, sub-stratify by the top-scoring JASPAR
motif present in the sequence (or "no strong motif"). Sample uniformly
across the resulting (class × dominant_motif) bins, capping high-frequency
bins. This adds a second axis of diversity beyond cCRE class.

Hypothesis: **010 > 006**. 006 already showed up-weighting rare classes
helps; up-weighting rare TF families within each class should help
further. If 010 < 006, then class-level stratification is sufficient
and TF-stratification adds noise. Either way it directly probes the
"motif diversity" arm of T5.
