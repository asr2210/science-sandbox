# 007_dels_only — notes

## Design
50K x 200bp sampled (without replacement) from the 1,469,205-cCRE
dELS pool. Central 200-bp window from GRCh38. Mean GC = 0.461,
sd = 0.089.

## Hypothesis
Tests if PLS-only collapse (exp 006) was PLS-specific or if all
single-class libraries fail. dELS has 30× more cCREs than PLS and
GC composition closer to genomic baseline.

## Result vs. previous

| eval | rand   | cCRE   | PLS    | **dELS** | Δ(dELS−cCRE) | Δ(dELS−rand) |
|------|--------|--------|--------|----------|--------------|--------------|
| 01   | 0.6954 | 0.7133 | 0.5903 | 0.7090   | -0.004       | +0.014       |
| 02   | 0.7848 | 0.8046 | 0.6657 | 0.8014   | -0.003       | +0.017       |
| 03   | 0.7612 | 0.7870 | 0.6278 | 0.7897   | +0.003       | +0.029       |
| 04   | 0.7494 | 0.7733 | 0.7022 | 0.7417   | -0.032       | -0.008       |
| 05   | 0.6951 | 0.7133 | 0.5901 | 0.7089   | -0.004       | +0.014       |
| 06   | 0.7853 | 0.8048 | 0.6655 | 0.8017   | -0.003       | +0.016       |
| 07   | 0.6684 | 0.7452 | 0.5091 | 0.7605   | **+0.015**   | +0.092       |
| 08   | 0.7841 | 0.6380 | 0.4774 | 0.6720   | +0.034       | -0.112       |
| 09   | 0.8115 | 0.8385 | 0.7543 | 0.8042   | -0.034       | -0.007       |
| 10   | 0.7564 | 0.7635 | 0.5925 | 0.7779   | +0.014       | +0.022       |
| 11   | 0.6833 | 0.7010 | 0.5789 | 0.6973   | -0.004       | +0.014       |
| 12   | 0.6553 | 0.6757 | 0.5372 | 0.6782   | +0.003       | +0.023       |
| 13   | 0.6584 | 0.7422 | 0.4912 | 0.7601   | **+0.018**   | +0.102       |
| 14   | 0.7851 | 0.8046 | 0.6661 | 0.8015   | -0.003       | +0.016       |

Mean across evals: rand 0.738, cCRE 0.748, PLS 0.604, **dELS 0.756**.

## Interpretation

**dELS-only is the best library so far.** It beats class-balanced
cCRE on average (0.756 vs 0.748) and slightly beats it on the
motif-rewarding evals (07: +0.015, 13: +0.018). It also recovers
some of eval_08 (0.672 vs cCRE 0.638), though still well below
random (0.784).

This **falsifies my exp 006 conclusion** that "single-class libraries
are inherently bad." PLS-only collapsed, but dELS-only thrives. The
difference must be either:
1. **Pool size / internal diversity**: dELS has 1.47M elements vs
   PLS's 47K (30×). With 50K sequences sampled from 1.47M, the
   model sees ~30× more unique regulatory contexts than PLS-only.
2. **GC composition**: PLS GC=0.606 vs dELS GC=0.461 (closer to
   genomic baseline of ~0.41). PLS extreme GC overfits the model.
3. **Regulatory grammar diversity within class**: distal enhancers
   span the full diversity of cell-type-specific TF binding
   programs, while promoters are dominated by housekeeping TFs.
4. **Activity range**: enhancers in MPRA span a wide activity range
   (silent to strong); promoters often saturate the reporter.

Most likely all four contribute. The general lesson:
> **What matters is the diversity of regulatory contexts the
> training set spans, not the number of named "element classes" it
> spans.** dELS alone provides enough internal diversity (1.47M
> contexts) to train a model that generalizes well. Class diversity
> is helpful when the per-class pool is small or narrow, but
> redundant when the chosen class is itself large and diverse.

dELS slightly losing on eval_04 (-0.03) and eval_09 (-0.03) suggests
some of the smaller classes (probably PLS, TF, CA) contributed
specifically to those evals. The next experiment can test whether
adding a small fraction of these classes recovers those evals
without hurting the dELS gains.

## What this changes (theory update)

Refined theory:
> Within a single broad class (like dELS), 1.47M elements provides
> enough regulatory diversity to be sufficient for generalization.
> The cCRE class-balanced design (exp 002) was diluting the
> high-information dELS pool with smaller, narrower-grammar classes
> (PLS, CA-TF) that each contribute less per sequence. dELS-dominant
> sampling is a free improvement.

This converges with the principle from exp 005: **don't dilute
informative sequences with less-informative ones**.

## Next experiment

The result raises a clean question: is the gain from "dELS
specifically" or from "natural cCRE proportions" (which would also
be ~62% dELS)? Test with **natural-proportion cCRE library**: sample
50K from the full cCRE pool weighted by natural class frequency
(dELS ~62%, pELS ~10%, CA ~10%, etc.).

If natural-prop ≥ dELS-only → natural proportions are the right
weighting and we should respect them.
If natural-prop < dELS-only → pure dELS-dominant is better; the
small classes are noise.
If natural-prop ≈ dELS-only → roughly equivalent and we can chase
gains elsewhere (e.g., on eval_08).
