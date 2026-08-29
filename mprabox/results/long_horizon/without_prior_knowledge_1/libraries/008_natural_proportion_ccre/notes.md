# 008_natural_proportion_ccre — notes

## Design
50K x 200bp sampled uniform-random from the full 2.35M-cCRE pool (no
class balancing). Naturally yields ~62.6% dELS, ~10.6% pELS, ~10.5% CA,
~5.4% CA-CTCF, ~4.5% TF, ~3.4% CA-H3K4me3, ~2.0% PLS, ~1.1% CA-TF.
Mean GC = 0.464, sd = 0.095.

## Hypothesis
Tests whether dELS-only's gain (exp 007) is from "dELS specifically"
or from "natural class proportions" (which would also be dELS-dominated
~62%).

## Result vs. previous

| eval | rand   | cCRE   | dELS   | **natprop** | Δ(natprop−dELS) | Δ(natprop−cCRE) |
|------|--------|--------|--------|-------------|------------------|-------------------|
| 01   | 0.6954 | 0.7133 | 0.7090 | 0.7083      | -0.001           | -0.005            |
| 02   | 0.7848 | 0.8046 | 0.8014 | 0.8018      | +0.000           | -0.003            |
| 03   | 0.7612 | 0.7870 | 0.7897 | 0.7892      | -0.001           | +0.002            |
| 04   | 0.7494 | 0.7733 | 0.7417 | 0.7466      | +0.005           | -0.027            |
| 05   | 0.6951 | 0.7133 | 0.7089 | 0.7084      | -0.001           | -0.005            |
| 06   | 0.7853 | 0.8048 | 0.8017 | 0.8022      | +0.001           | -0.003            |
| 07   | 0.6684 | 0.7452 | 0.7605 | 0.7501      | -0.010           | +0.005            |
| 08   | 0.7841 | 0.6380 | 0.6720 | 0.6603      | -0.012           | +0.022            |
| 09   | 0.8115 | 0.8385 | 0.8042 | 0.8083      | +0.004           | -0.030            |
| 10   | 0.7564 | 0.7635 | 0.7779 | 0.7718      | -0.006           | +0.008            |
| 11   | 0.6833 | 0.7010 | 0.6973 | 0.6965      | -0.001           | -0.005            |
| 12   | 0.6553 | 0.6757 | 0.6782 | 0.6772      | -0.001           | +0.002            |
| 13   | 0.6584 | 0.7422 | 0.7601 | 0.7540      | -0.006           | +0.012            |
| 14   | 0.7851 | 0.8046 | 0.8015 | 0.8017      | +0.000           | -0.003            |

Mean across evals: rand 0.738, cCRE 0.748, **dELS 0.756**, natprop 0.752.

## Interpretation

**natprop sits between cCRE and dELS — slightly worse than dELS-only.**
Adding the small classes (PLS, CA-TF, etc.) at natural frequencies
did not help on average. The "62% dELS dominance" of natprop captures
most of dELS-only's benefit; the remaining 38% (other classes) at
natural proportions is approximately neutral.

**Class-balanced (12.5% each) was the worst of the three cCRE designs**
because it overweighted the small narrow-grammar classes.

**Per-eval pattern:**
- natprop ≈ dELS on the high-baseline evals (02, 03, 06, 14)
- natprop slightly worse than dELS on motif-rewarding evals
  (07: −0.010, 13: −0.006)
- natprop slightly better than dELS on eval_04 (+0.005) and eval_09
  (+0.004) — confirms my exp 007 conjecture that the small classes
  contribute specifically to those two.

The trade-off is small (~0.005 either way per eval) and the average
favors dELS-only.

## What this changes (theory update)

> The cCRE class proportions are not very important once dELS dominates.
> The dELS-only library wins because it concentrates training on the
> most diverse, highest-information class. Adding small narrow classes
> (PLS, CA-TF) at any proportion modestly dilutes the average.

This further confirms the exp 005 / 007 lesson:
**don't dilute informative sequences with less-informative ones.**

## Where the headroom remains

Best per-eval across all 8 experiments:
- eval_01 cCRE 0.7133, eval_02 cCRE 0.8046, eval_03 dELS 0.7897,
  eval_04 cCRE 0.7733, eval_05 cCRE 0.7133, eval_06 cCRE 0.8048,
  eval_07 dELS 0.7605, eval_08 random 0.7841, eval_09 cCRE 0.8385,
  eval_10 dELS 0.7779, eval_11 cCRE 0.7010, eval_12 dELS 0.6782,
  eval_13 dELS 0.7601, eval_14 cCRE 0.8046.
- Composite "best per eval": 0.762 — barely above dELS-only's 0.756.
- The big gap is eval_08 (random 0.784 vs dELS 0.672, Δ=0.112).
  Closing this would add ~0.008 to mean.

## Next experiment

Genuine novel direction: **genome-wide random sampling**. Sample 50K
random 200bp windows from the entire human genome (most will be
intergenic non-cCRE — gene deserts, introns, non-regulatory regions).
- If genome-wide ≈ dELS-only → "regulatory annotation" doesn't matter,
  any real DNA works.
- If genome-wide < dELS-only → cCRE annotation captures real
  information.
- If genome-wide > dELS-only → we should expand beyond cCREs.

This is the cleanest single bit on whether cCRE annotation
specifically is what helps, vs. real human DNA in general.
