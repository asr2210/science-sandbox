# 010 — TF-motif × cCRE-class stratified

## Design
Within each cCRE class, sub-stratify by dominant JASPAR motif from 20
TF-family archetypes (CTCF, SP1, FOS, NFKB1, STAT1, GATA1, FOXA1,
HNF4A, TEAD1, E2F1, MAX, Pou5f1::Sox2, TP53, RUNX1, LEF1, SOX2, EGR1,
HOXA9, NR3C1, ATF3) plus a "no strong motif" (BG) bucket. PWM scoring
in pure numpy with log-odds threshold 6.0 bits-equivalent. Pre-scan
200K cCREs (25K per class), bin by (class × top-motif), sample with
per-bin cap 320 and top-up from leftovers.

168 (class × motif) bins observed. Top bins: PLS-SP1 (~7.5K), CA-TF-FOS
(~3.6K), dELS-RUNX1 (~3.5K), pELS-RUNX1 (~3.4K), PLS-EGR1 (~3.4K).

## Results (mean over 3 seeds)
- eval_01 = **0.7122** (vs 006 0.7368 = **−0.025**; vs 002 0.7263 = **−0.014**)
- mean across 14 evals ≈ **0.7493** (vs 006 0.7754 = **−0.026**; vs 002 0.7665 = −0.017)

## Per-eval delta vs 006 (cCRE class-stratified)
01:−0.025 02:−0.025 03:−0.025 04:−0.018 05:−0.024 06:−0.025 07:−0.032
08:−0.036 09:−0.020 10:−0.027 11:−0.024 12:−0.023 13:−0.036 14:−0.025

**Loses on ALL 14 evals**, by 0.018–0.036. Largest losses on eval_07,
eval_08, eval_13 — these are exactly the evals where 006 already
underperformed slightly. TF-stratification made them worse.

## Per-eval delta vs 002 (cCRE uniform)
01:−0.014 02:−0.014 03:−0.018 04:**+0.010** 05:−0.014 06:−0.015
07:−0.035 08:−0.041 09:**+0.014** 10:−0.028 11:−0.015 12:−0.016
13:−0.041 14:−0.014

10 wins on eval_04 (+0.010) and eval_09 (+0.014) — these are evals
that previously responded well to class-stratification (006 vs 002:
+0.028 and +0.034). The TF-stratification preserved some of the gain
on these but lost it elsewhere.

## Across-seed
eval_01: 0.6953 / 0.7079 / 0.7334 → SD ≈ 0.019. Lower variability
than 002/006, but the absolute level is lower.

## Branching outcome
Pre-experiment, three outcomes were defined:
- 010 > 006 → TF diversity helps beyond class diversity (extends T5)
- 010 ≈ 006 → cCRE class already captures the relevant axis
- 010 < 006 → forcing TF balance dilutes natural cCRE composition

Result: **010 < 006**, the third branch. Forcing per-(class × TF)
balance over-represents rare motif combinations that may be poorly
calibrated regulatory elements. The "natural" within-class motif
distribution carries informative signal that uniform-bin sampling
breaks.

## What this updates in the theory
**T5 (refined again):** Class-level diversity (cCRE class) helps
because rare classes still represent **well-formed regulatory units**.
TF-level "diversity" (uniform per-(class × motif) sampling) hurts
because most rare (class × motif) bins contain unusual combinations
that are not representative MPRA training material — e.g., dELS with
strong TP53 motif, or CA-CTCF with no strong CTCF motif (the BG bin
in CA-CTCF). Stratification is informative ONLY when bins correspond
to coherent biological categories.

**T8 (new):** Diversity-by-stratification has diminishing returns and
eventually goes negative. cCRE class (8 categories) → +0.013 (006).
cCRE class × TF (168 categories) → −0.026 (010). Too-fine
stratification creates bins of biologically-noisy sequences and
dilutes the signal-rich majority. **Optimal stratification axis is
the coarsest one that still captures meaningful diversity.**

This mirrors the 007 lesson at the motif scale: just as random
dilutes cCRE signal, fine-grained TF-binning dilutes within-class
coherence.

## Best library so far
006 stratified, mean ≈ 0.7754. Unchanged. Strongly held: now we have
two falsified attempts (007 mixing in random, 010 finer stratification).

## Most informative next experiment (011)
**Test the OPPOSITE direction: coarser stratification.** 006 used 8
cCRE classes; collapse to **3 super-classes**: promoters (PLS +
pELS + CA-H3K4me3), distal-enhancers (dELS + CA + TF), insulators-and-
TF-only (CA-CTCF + CA-TF). 50K with equal counts per super-class.
- 011 ≈ 006 → 8-vs-3 categorization is neutral; what matters is
  having multiple buckets, not how many.
- 011 > 006 → coarser is better (T8 strict reading: **even coarser**)
- 011 < 006 → 8 is better calibrated than 3; the 8 cCRE classes ARE
  the right axis (T8 nuanced reading: class is the right unit).

Either way it tightly bounds T8. After 011 we can move on to other
axes (sequence length, motif augmentation strategies, etc.).
