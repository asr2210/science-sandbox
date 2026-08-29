# 007 — stratified cCRE (40K) + uniform random (10K) mix

## Design
40K stratified cCREs (5K per class × 8 classes) + 10K uniform random
200bp sequences. Test: does mixing recover eval_08 coverage hole
without sacrificing too much elsewhere?

## Results (mean over 3 seeds)
- eval_01 = **0.7276** (vs 006 strat 0.7368 = **−0.009**)
- mean across 14 evals ≈ **0.7672** (vs 006 ≈ 0.7754, **−0.008**)

## Per-eval delta vs 006
01:−0.009 02:−0.009 03:−0.008 04:−0.012 05:−0.009 06:−0.009 07:−0.016
08:**+0.019** 09:−0.013 10:−0.009 11:−0.009 12:−0.008 13:−0.013 14:−0.009

eval_08 RECOVERED (+0.019), going from 0.682 → 0.702. Every other
eval LOST ~0.01. Net loss of 0.008 averaged.

## Interpretation
The eval_08 hole in pure cCRE libraries is real, and it can be
partially recovered by adding random sequences. But random adds
"noise" that hurts the 13 other evals more than eval_08 helps.

This suggests:
- eval_08 measures something different from the other 13 evals (likely
  broad-coverage / synthetic / diverse-composition sequences)
- The remaining 13 evals favor pure regulatory content
- The optimal aggregate library is concentrated on regulatory elements;
  the eval_08 outlier should be tolerated, not chased

## Across-seed
eval_01: 0.7304 / 0.6852 / 0.7671 → SD ≈ 0.034. High variability;
adding 10K random per seed introduces a new noise source.

## What this updates in T5/T6

**T6:** A library is informative in proportion to the fraction of
sequences from real regulatory elements. Diluting with random reduces
the model's exposure to motif-grammar examples. eval_08-like coverage
demands are best met within the regulatory pool (e.g., extreme TF
diversity), not by adding random.

## Most informative next experiment (008)
**Switch annotation source: DHS Index uniform sample.** The Meuleman
2020 DHS Index has 3.5M DNase-hypersensitive sites with NMF-decomposed
cell-type loadings, distinct from ENCODE cCRE pipeline. Different
selection criteria may capture different regulatory diversity.
- 008 ≈ 002 → cCRE vs DHS source doesn't matter
- 008 > 006 → DHS captures more useful regulatory diversity than cCRE
- 008 < 002 → DHS is noisier; cCREs are better-curated for ML
This is a sister-comparison and lets me decide which annotation source
to invest further iterations in.
