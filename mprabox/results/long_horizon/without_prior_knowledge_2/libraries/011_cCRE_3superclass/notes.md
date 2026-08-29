# 011 — cCRE 3-superclass stratified (coarser than 006)

## Design
8 cCRE classes collapsed to 3 functional super-classes:
- promoter:  PLS + pELS + CA-H3K4me3 (376K elements)
- distal:    dELS + CA + TF (1.82M)
- insul_tf:  CA-CTCF + CA-TF (152K)

50K with equal counts per super-class (~16,667 each), 200bp on midpoint.
Tests T8: is the right stratification axis 3 (coarser), 8 (006), or
168 (010, finer)?

## Results (mean over 3 seeds)
- eval_01 = **0.7286** (vs 006 0.7368 = **−0.008**)
- mean across 14 evals ≈ **0.7715** (vs 006 0.7754 = **−0.004**)

## Per-eval delta vs 006 (8-class stratified)
01:−0.008 02:−0.006 03:−0.003 04:−0.015 05:−0.008 06:−0.006 07:**+0.006**
08:**+0.010** 09:−0.018 10:**+0.005** 11:−0.007 12:−0.003 13:**+0.006** 14:−0.006

**Wins on 4 evals (07, 08, 10, 13)** — exactly the four evals where 006
underperformed slightly. Loses on the other 10 by small amounts.

Eval-range:
- 011 spread: 0.6924 to 0.8395 = 0.147
- 006 spread: 0.6822 to 0.8574 = 0.175
**011 is more uniform** across evals; 006 is higher-variance with a
higher peak.

## Across-seed
eval_01: 0.7457 / 0.6926 / 0.7476 → SD ≈ 0.025. Similar to 006.

## Branching outcome
Pre-experiment branches:
- 011 ≈ 006 → granularity neutral (no, they differ ~0.004 on mean)
- 011 > 006 → coarser strictly better (no)
- 011 < 006 → 8-class is the right unit (mostly yes, but only barely)

Result: **011 is between 010 (much worse, 168 bins) and 006 (best, 8
bins) but VERY close to 006 (−0.004).** The 8-class axis IS approximately
right — both finer (010, −0.026) and coarser (011, −0.004) lose.

Crucially, the loss vs 006 is small but the eval-distribution is
different: 011 is flatter. There's a Pareto trade-off — 006 maximizes
mean and dominant-eval performance; 011 trades some peak performance
for uniformity.

## What this updates in T8
**T8 (refined):** Stratification has a sweet spot — too coarse loses
the meaningful biological diversity, too fine creates biologically-noisy
bins. For ENCODE V4 cCREs, 8 classes is at or very near optimum;
3-superclass is only 0.004 below; 168 (class × motif) is 0.026 below.

**T9 (new — Pareto-style observation):** Eval-set heterogeneity means
"best library" depends on weighting:
- Maximize mean → 006 (8-class)
- Maximize uniformity (low min) → 011 (3-superclass)
- Maximize eval_01 specifically → 006

The eval_07/08/10/13 cluster appears to favor **broader sequence
coverage** (random in 005, super-classes in 011 both help), while
eval_01-06/09/11/12/14 cluster favors **fine-grained class signal**.
These appear to be two distinct evaluation modes.

## Best library so far
006 stratified (8-class), mean ≈ 0.7754. Confirmed near-optimum.

## Most informative next experiment (012)
**Per-class up-weighting (rare-class boost) within 8-class scheme.**
006 used equal counts (6,250 each). What if we further upweight the
RAREST classes (CA-TF=26K, PLS=48K) at the cost of dELS (1.47M)?

Specifically: try 8K each for PLS, CA-CTCF, CA-TF, CA-H3K4me3 (the
4 rare classes) and 4.5K each for pELS, dELS, CA, TF (the 4 abundant).
Total 32K + 18K = 50K. Hypothesis: if rare-class signal is
information-limited (fewer training examples per class causing model
underfitting on those contexts), upweighting helps.

- 012 > 006 → rare-class info was the bottleneck (extends T8: equal
  counts are not optimal; INVERSE-frequency upweighting helps)
- 012 ≈ 006 → 6,250 was already saturating per-class signal
- 012 < 006 → forcing more rare-class examples diluted with redundant/
  noisy sequences (the rare class pool isn't 8K-deep in unique signal)

This directly probes whether the per-class learning curve is still
rising at 6,250 examples.
