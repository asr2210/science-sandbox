# 016 — cCRE 1/sqrt(pool_size) per-class weighting

## Design
Per-class counts proportional to 1/sqrt(pool_size):
PLS=9148, CA-CTCF=5618, CA-TF=12344, CA-H3K4me3=7085,
pELS=3993, dELS=1645, CA=4021, TF=6146 (sum=50K).

Tests T8/T10: does class info-density really scale as 1/sqrt(pool)?

## Results (mean over 3 seeds)
- eval_01 = **0.7294** (vs 013 0.7477 = **−0.018**)
- mean across 14 evals ≈ **0.7694** (vs 013 0.7900 = **−0.021**)

## Per-eval delta vs 013
01:−0.018 02:−0.019 03:−0.020 04:−0.015 05:−0.018 06:−0.019 07:−0.027
08:−0.032 09:−0.017 10:−0.024 11:−0.018 12:−0.018 13:−0.023 14:−0.019

**Loses on ALL 14 evals**, by 0.015–0.032. Average −0.021.

## Per-class delta vs 013 (count change → effect)
- PLS: 10K → 9.1K (−9%)
- CA-CTCF: 10K → 5.6K (**−44%**)  ← biggest single change
- CA-TF: 10K → 12.3K (+23%)
- CA-H3K4me3: 10K → 7.1K (−29%)
- pELS: 2.5K → 4.0K (+60%)
- dELS: 2.5K → 1.6K (−34%)
- CA: 2.5K → 4.0K (+61%)
- TF: 2.5K → 6.1K (+146%)

## Across-seed
eval_01: 0.7000 / 0.7592 / 0.7290 → SD ≈ 0.030. **Higher** than 013's
0.008. Smaller pool fractions → more sampling noise.

## Branching outcome
Pre-experiment branches:
- 016 > 013 → 1/sqrt-pool is the right principle (no)
- 016 ≈ 013 → 013's coarse split is sufficient (no, 016 lost 0.021)
- 016 < 013 → CA-CTCF info is high even with large pool (yes)

Result: **016 ≪ 013, falsifies the 1/sqrt-pool principle.** The biggest
losses (eval_07/08/13) coincide with the largest single count change
(CA-CTCF dropped 44%). CA-CTCF — despite a 126K pool — is
information-dense and behaves like a rare class.

## What this updates in the theory
**T10 (revised):** Class info-density is NOT a simple function of pool
size. CA-CTCF (126K pool) is as information-dense as CA-TF (26K pool).
Conjecture: information-density is determined by **functional
specificity** of the class, not its pool size. CA-CTCF has highly
specific CTCF-binding signatures; CA-TF has highly specific TF
combinations. dELS (1.47M pool) is information-sparse because dELS
covers a heterogeneous mix of distal regulatory contexts.

**T8 (refined): functional grouping > pool-size grouping.** The
"rare" cluster in 013 = {PLS, CA-CTCF, CA-TF, CA-H3K4me3} happens to
align with **functionally specific** cCRE classes (promoter-like,
CTCF, TF-only, H3K4me3-marked CA). The "abundant" cluster =
{pELS, dELS, CA, TF} happens to be heterogeneous-enhancer-like
plus generic-CA/TF. The 013 partition was lucky/correct because it
isolated functional-specificity, not pool-size.

**T13 (new — principled stratification design):** Stratification
weights should reflect **functional specificity**, not pool size.
For 8 ENCODE cCRE classes, the optimal split is approximately
{PLS, CA-CTCF, CA-TF, CA-H3K4me3} = high-spec at 10K each;
{pELS, dELS, CA, TF} = low-spec at 2.5K each.

## Best library so far
**013 cCRE extreme upweight (10K/2.5K), mean ≈ 0.7900**. Still best.
The 1/sqrt-pool refinement does not help; the functional-specificity
grouping was the right move.

## Most informative next experiment (017)
**Switch to a fundamentally orthogonal axis: motif augmentation on
top of 013.** Take 013-style cCRE samples (10K rare / 2.5K abundant)
and for each, insert one randomly-sampled JASPAR archetype motif at a
random position (overwriting 6-15 native bases). Tests whether motif
density adds independent signal on top of the optimal class-balance.

- 017 > 013 → motif density is a separate informative axis (extends
  T5; suggests 013 is motif-limited)
- 017 ≈ 013 → cCRE motif content is already saturated
- 017 < 013 → forced motif insertion disrupts native cCRE grammar
  (consistent with 004's "motif in random scaffold" failure: forced
  motif placement is harmful when surrounding context matters)

This cleanly tests T5 (motif-axis) on the new best library, separating
"motif availability" from "regulatory context" — two arms of T5 that
were always conflated before.
