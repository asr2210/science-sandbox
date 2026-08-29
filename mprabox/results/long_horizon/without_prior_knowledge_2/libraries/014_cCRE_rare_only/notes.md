# 014 — cCRE rare-only (12.5K each, 4 rare classes, no abundant)

## Design
12,500 each from PLS, CA-CTCF, CA-TF, CA-H3K4me3 = 50K. The 4 abundant
classes (pELS, dELS, CA, TF) get ZERO. Tests the limit of the
inverse-frequency gradient: is rare-only the optimum?

## Results (mean over 3 seeds)
- eval_01 = **0.6856** (vs 013 0.7477 = **−0.062**)
- mean across 14 evals ≈ **0.7155** (vs 013 0.7900 = **−0.075**)

## Per-eval delta vs 013
01:−0.062 02:−0.070 03:−0.075 04:−0.053 05:−0.062 06:−0.069 07:**−0.102**
08:**−0.112** 09:−0.060 10:−0.082 11:−0.061 12:−0.065 13:**−0.100** 14:−0.069

**LOSES on ALL 14 evals** by 0.053–0.112. Average **−0.075**. Largest
losses on the broad-coverage cluster (eval_07, 08, 13). Even eval_09
(which favored rare classes) drops by 0.060.

## Across-seed
eval_01: 0.6856 / 0.6891 / 0.6821 → SD ≈ 0.003. Extremely stable, but
stably much worse. Large pool reduction means low seed variance.

## Branching outcome
Pre-experiment branches:
- 014 > 013 → rare-only is the limit, abundant contribute nothing
- 014 ≈ 013 → abundant near-negligible at 2.5K
- 014 < 013 → abundant contribute irreducible signal even at 2.5K

Result: **014 ≪ 013, much worse than expected.** The abundant classes
(esp. dELS distal enhancers) provide critical context that cannot be
substituted by more rare-class examples. The −0.075 drop is among the
largest single-experiment regressions in the project.

## What this updates in the theory
**T8 (final form for cCRE-classification axis):** The inverse-frequency
optimum is BETWEEN 006 (equal 6.25K) and 014 (rare-only 12.5K).
Specifically, 013 (10K rare / 2.5K abundant) sits inside this interval
and is the best so far. The gradient from 006 → 012 → 013 was monotone
positive, but pushing all the way to 014 falls off a cliff. Optimum
is around 10-11K rare / 2-3K abundant.

**T11 (new — abundant-class minimum):** Abundant cCRE classes have a
floor count below which performance collapses, even though most of
their elements are redundant. Hypothesis: abundant classes contribute
**genomic context diversity** that rare classes cannot — promoter-
distal mixing, intergenic enhancer variants, etc. — that the model
needs to interpolate between rare-class regulatory archetypes.
2.5K (013) was near the floor; 0K (014) collapses.

**T12 (new — broad-coverage cluster needs abundant):** The eval_07/08/13
cluster (T9 broad-coverage) lost the most from removing abundant
classes (−0.10 each). This is consistent with the hypothesis that
those evals probe sequence-space coverage that requires distal-enhancer
diversity (most of dELS).

## Best library so far
**013 cCRE extreme upweight, mean ≈ 0.7900**. Holds. Abundant classes
at 2.5K are necessary; 0K is too few.

## Most informative next experiment (015)
**Tighten the bracket on the optimum.** Try **11K rare / 1.5K abundant**
— between 013 (10K/2.5K, mean 0.7900) and 014 (12.5K/0K, mean 0.7155).
- 015 > 013 → optimum is between 11K-12K rare; sharper peak than seen
- 015 ≈ 013 → 10K rare is at saturation; 1.5K abundant still enough
- 015 < 013 → 2.5K abundant is the floor; 1.5K starts to collapse
  (consistent with T11 floor effect appearing earlier than expected)

Pinpoints where the inverse-frequency curve plateaus and where the
abundant-class floor kicks in.
