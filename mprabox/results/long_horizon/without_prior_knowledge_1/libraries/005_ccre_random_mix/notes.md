# 005_ccre_random_mix — notes

## Design
50K = 25K cCRE-derived (class-balanced over 8 SCREEN classes,
3,125 per class) + 25K uniform-random ACGT, shuffled together.

## Hypothesis
If composition coverage (random) and motif content (cCRE) are additive,
the mixture should be roughly best-of-both: ≈ random on eval_08,
≈ cCRE on motif-rewarding evals 07/13, ≥ cCRE elsewhere.

## Result vs. previous

| eval | rand   | cCRE   | motif  | **mix**| Δ(mix-rand) | Δ(mix-cCRE) |
|------|--------|--------|--------|--------|-------------|-------------|
| 01   | 0.6954 | 0.7133 | 0.6861 | 0.6951 | -0.000      | -0.018      |
| 02   | 0.7848 | 0.8046 | 0.7754 | 0.7860 | +0.001      | -0.019      |
| 03   | 0.7612 | 0.7870 | 0.7503 | 0.7668 | +0.006      | -0.020      |
| 04   | 0.7494 | 0.7733 | 0.7408 | 0.7461 | -0.003      | -0.027      |
| 05   | 0.6951 | 0.7133 | 0.6856 | 0.6952 | +0.000      | -0.018      |
| 06   | 0.7853 | 0.8048 | 0.7759 | 0.7861 | +0.001      | -0.019      |
| 07   | 0.6684 | 0.7452 | 0.6636 | 0.7026 | +0.034      | -0.043      |
| 08   | 0.7841 | 0.6380 | 0.7679 | 0.6872 | -0.097      | +0.049      |
| 09   | 0.8115 | 0.8385 | 0.8029 | 0.8077 | -0.004      | -0.031      |
| 10   | 0.7564 | 0.7635 | 0.7565 | 0.7399 | -0.017      | -0.024      |
| 11   | 0.6833 | 0.7010 | 0.6743 | 0.6827 | -0.001      | -0.018      |
| 12   | 0.6553 | 0.6757 | 0.6454 | 0.6590 | +0.004      | -0.017      |
| 13   | 0.6584 | 0.7422 | 0.6460 | 0.6999 | +0.042      | -0.042      |
| 14   | 0.7851 | 0.8046 | 0.7760 | 0.7859 | +0.001      | -0.019      |

Mean across evals: rand 0.738, cCRE 0.748, motif 0.732, **mix 0.738**.

## Interpretation

**Mixture is roughly the linear midpoint of pure cases on most evals.**
For motif-rewarding evals 07/13, mixture is at ~midpoint of (rand,
cCRE). For eval_08, mixture is between random (0.78) and cCRE (0.64),
closer to cCRE side. Net effect: mixture ≈ random on average.

The "additive best-of-both" hypothesis is **falsified**. Mixing
biology with random doesn't combine the strengths — it dilutes both.

This is an important practical lesson: **adding uniform random to a
biological library actively hurts it.** The 25K random sequences in
the mix took up half the model's training capacity but added negative
information for most evals, only helping eval_08 partially.

The mixture diagnoses the real tradeoff:
- To improve eval_07/13, the model needs DENSE biological motif
  content — 50% biological isn't enough to fully convey the signal.
- To improve eval_08, the model needs UNIFORM composition exposure —
  but adding random doesn't selectively help eval_08; it dilutes
  everywhere.
- These two demands appear to compete for model capacity.

## What this changes (theory update)

> Library types do NOT additively combine. A mixture of 50% A + 50% B
> performs roughly like a midpoint, sometimes worse on average than
> either pure A or pure B. Each sequence in the library competes
> for model training capacity — adding non-informative sequences
> reduces the signal density of informative ones.

This implies: **the right strategy is to enrich the library with
maximally-informative sequences and not waste slots on
"diversification" via random/non-informative sequences.**

The eval_08 problem is real and may not be solvable while
maintaining cCRE-level performance on the rest. It might require a
qualitatively different library type that has both motif content AND
uniform composition — not a mixture of two libraries.

## Next experiment

The mixture hypothesis is dead. Better question: among the cCRE
classes (dELS, pELS, PLS, ...), which contribute most to the
motif-rewarding gains? Test: **PLS-only library (50K promoter-like
sequences, oversampled from the 47,532 PLS pool).**

If PLS-only ≥ class-balanced cCRE on eval_07/13 → promoter-class is
sufficient and we should enrich that.
If PLS-only < class-balanced cCRE → diversity across element classes
matters (dELS / pELS / TF / CA) and we should keep the balance.
If PLS-only ≈ class-balanced → class doesn't matter, the gain is
broadly distributed.
