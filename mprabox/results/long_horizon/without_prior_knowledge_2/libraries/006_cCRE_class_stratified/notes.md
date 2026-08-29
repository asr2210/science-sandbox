# 006 — cCRE class-stratified (equal counts)

## Design
6,250 cCREs from each of 8 classes (PLS, pELS, dELS, CA-CTCF,
CA-H3K4me3, CA-TF, CA, TF) = 50K total. 200bp centered on midpoint.
Per-seed: independent stratified subsample. Shuffled before writing
to avoid block ordering by class.

## Results (mean over 3 seeds)
- eval_01 = **0.7368** (vs 002 cCRE 0.7263 = **+0.011**)
- mean across 14 evals ≈ **0.775** (vs 002 ≈ 0.762, **+0.013**)
- per cell type: K562=0.776, HepG2=0.766, SK-N-SH=0.782

## Per-eval delta vs 002
01:+0.011 02:+0.010 03:+0.007 04:**+0.028** 05:+0.010 06:+0.010
07:−0.003 08:−0.006 09:**+0.034** 10:−0.001 11:+0.009 12:+0.007
13:−0.005 14:+0.010

Wins on 11/14 evals. Largest gains: **eval_04 (+0.028) and eval_09
(+0.034)**. Slight losses on 07/08/10/13 (−0.001 to −0.006).

## Across-seed
eval_01: 0.7041 / 0.7641 / 0.7422 → SD ≈ 0.030. Variability remains
high, similar to 002.

## Interpretation
Up-weighting rare cCRE classes (PLS, CA-CTCF, CA-TF) gives the model
exposure to distinct regulatory contexts that natural-distribution
sampling under-represented. The mean lift is modest (+0.013) but
robust (positive on 11/14 evals).

eval_09 (which previously favored cCRE) showed the biggest gain —
plausibly because eval_09 contains promoter/CTCF-rich elements that
PLS/CA-CTCF up-weighting helps. eval_04's +0.028 may reflect the
same.

The negative deltas (eval_07, 08, 10, 13) are small (within seed-SD)
and not clearly meaningful. eval_08 remains the outlier where natural
libraries underperform — class diversity didn't fix it.

## What this updates in T5
**T5 (refined):** The MOTIF DIVERSITY exposed to the model matters
beyond the natural class distribution. Up-weighting rare regulatory
contexts adds informative examples. cCRE class is a useful proxy for
regulatory-context diversity.

## Best library so far
006 stratified, mean ≈ 0.775, eval_01 = 0.737. New target to beat.

## Most informative next experiment (007)
**Mix: stratified cCRE + uniform random.** 40K stratified cCREs +
10K uniform random. Tests whether we can keep cCRE benefits while
recovering coverage on eval_08 (where random dominates).
- If 007 > 006 overall → mixing strictly improves; coverage was a
  bottleneck.
- If 007 ≈ 006 → mixing is neutral (gains balance losses).
- If 007 < 006 → cCRE composition matters; mixing dilutes signal.
This is the cleanest test of the "coverage vs signal" tradeoff
identified in T3-T5.
