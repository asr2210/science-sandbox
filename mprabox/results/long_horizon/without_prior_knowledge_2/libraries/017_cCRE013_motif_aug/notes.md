# 017 — cCRE 013 + motif augmentation

## Design
013-style cCRE samples (10K each rare: PLS, CA-CTCF, CA-TF,
CA-H3K4me3; 2.5K each abundant: pELS, dELS, CA, TF). For each 200bp
sequence, sample one of 20 JASPAR archetype motifs uniformly, sample
an instance from the PFM column probabilities, overwrite a
random-position window of length W (motif width, 6-18bp).

## Results (mean over 3 seeds)
- eval_01 = **0.7200** (vs 013 0.7477 = **−0.028**)
- mean across 14 evals = **0.7595** (vs 013 0.7900 = **−0.031**)

## Per-eval delta vs 013
01:−0.028 02:−0.030 03:−0.033 04:−0.024 05:−0.028 06:−0.030 07:−0.041
08:−0.031 09:−0.027 10:−0.025 11:−0.027 12:−0.029 13:−0.043 14:−0.030

**Loses on ALL 14 evals**, by 0.024–0.043. Largest losses on
broad-coverage cluster (eval_07, eval_13). Average −0.031.

## Across-seed
eval_01: 0.6886 / 0.7531 / 0.7182 → SD ≈ 0.026 (vs 013's 0.008).
Random motif insertion adds across-seed variance.

## Branching outcome
Pre-experiment branches:
- 017 > 013 → motif density is a separate informative axis (no)
- 017 ≈ 013 → cCRE motif content already saturated (no)
- 017 < 013 → forced motif insertion disrupts native cCRE grammar (yes)

Result: **017 ≪ 013, falsifies "motif-density-as-orthogonal-axis"
hypothesis.** Same shape as 004 (motif in random scaffold = 0.6824),
where motifs in non-native context hurt. Insertion at random position,
even within a real cCRE, is non-native context.

## What this updates in the theory
**T5 (refined — context-dependence law):** motif-axis informativeness
is NOT independent of context. Experiments 004, 010, 017 each tried
to add motif content to a base library and ALL HURT:
- 004: motif in random scaffold (0.6824) << random (0.7321)
- 010: motif-balanced cCRE (0.7493) << uniform cCRE (0.7619)
- 017: motif inserted into 013 (0.7595) << 013 (0.7900)

The model only learns motif→activity from sequences where the motif
sits in its NATIVE context. Forced placement either (a) breaks the
context the motif depends on, or (b) creates implausible
motif-context combinations the model would not see in test data.

**T14 (new — context-dependence is paramount):** For a sequence-to-
activity model that must generalize to held-out cell types, motif
informativeness comes from native context, not raw motif density.
The model needs to learn motif × context conditional dependencies,
which require natural co-occurrence statistics. Library design
should preserve native sequence grammar; constructing artificial
sequences (insertions, scaffolds, shuffles) discards that grammar.

This consolidates findings from {001, 003, 004, 010, 017}: every
experiment that breaks native sequence grammar loses to the
corresponding natural baseline, regardless of how the artificial
sequences were constructed.

## Best library so far
**013 cCRE extreme upweight (10K/2.5K), mean ≈ 0.7900**. Holds.

## Most informative next experiment (018)
**DHS-class upweighting analog of 013.** The Meuleman DHS Index has
each site labeled with a primary NMF component (1-16; broad cell-type
vocabulary like Lymphoid, Cardiac, Neural). Component sizes are
skewed. Apply 013's principle (upweight rare components) to DHS:
take ~12-13K from each rare component, ~1-2K from each abundant.

- 018 > 013 → rare-class upweighting principle generalizes beyond
  cCRE; DHS + cell-type stratification is even better (suggests T8
  → T15: principle is universal across regulatory atlases)
- 018 ≈ 013 → DHS gives same result as cCRE; the principle is
  agnostic to atlas
- 018 < 013 → DHS atlas is intrinsically less informative than cCRE
  even with the same rebalancing principle (consistent with 002 vs 008)

This is the cleanest "principle generalization" test on the table.
