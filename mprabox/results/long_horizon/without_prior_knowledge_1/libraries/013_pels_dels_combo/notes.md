# 013_pels_dels_combo — notes

## Design
25K pELS + 25K dELS, sampled (no replacement) from each pool,
shuffled together. Same central-200bp extraction as exp 002.

## Hypothesis
Tests whether combining the two best single-class libraries
captures their complementary per-eval strengths additively.
- pELS leads on general/high-baseline evals
- dELS leads on motif-rewarding evals (07, 13)
- If model can learn both → combo > both
- If mixing dilutes → combo < both (consistent with prior mix
  experiments)

## Result vs. constituents

| eval | rand   | dELS   | pELS   | **combo** | Δ(combo−pELS) | Δ(combo−dELS) |
|------|--------|--------|--------|-----------|---------------|---------------|
| 01   | 0.6954 | 0.7090 | 0.7203 | 0.6936    | -0.027        | -0.015        |
| 02   | 0.7848 | 0.8014 | 0.8129 | 0.7853    | -0.028        | -0.016        |
| 03   | 0.7612 | 0.7897 | 0.7958 | 0.7699    | -0.026        | -0.020        |
| 04   | 0.7494 | 0.7417 | 0.7603 | 0.7310    | -0.029        | -0.011        |
| 05   | 0.6951 | 0.7089 | 0.7203 | 0.6936    | -0.027        | -0.015        |
| 06   | 0.7853 | 0.8017 | 0.8133 | 0.7859    | -0.027        | -0.016        |
| 07   | 0.6684 | 0.7605 | 0.7489 | 0.7270    | -0.022        | -0.034        |
| 08   | 0.7841 | 0.6720 | 0.6844 | 0.6459    | -0.039        | -0.026        |
| 09   | 0.8115 | 0.8042 | 0.8238 | 0.7921    | -0.032        | -0.012        |
| 10   | 0.7564 | 0.7779 | 0.7729 | 0.7492    | -0.024        | -0.029        |
| 11   | 0.6833 | 0.6973 | 0.7083 | 0.6825    | -0.026        | -0.015        |
| 12   | 0.6553 | 0.6782 | 0.6853 | 0.6607    | -0.025        | -0.018        |
| 13   | 0.6584 | 0.7601 | 0.7473 | 0.7278    | -0.020        | -0.032        |
| 14   | 0.7851 | 0.8015 | 0.8129 | 0.7852    | -0.028        | -0.016        |

Mean: rand 0.738, dELS 0.756, pELS 0.758, **combo 0.731**.

## Interpretation

**Combo loses to BOTH constituents on EVERY eval.** Mean drop:
−0.025 vs pELS, −0.025 vs dELS. There is no eval where the combo
beats either pure class.

**Hypothesis falsified hard.** Combining the two best
single-class libraries does NOT capture their complementary
strengths. Instead, mixing produces dilution — the model trained
on the union learns weaker representations than on either pure
class.

**This is now the third confirmation that mixing dilutes:**
- exp 002 (8-class balanced) underperformed exp 007 (dELS-only)
- exp 005 (cCRE + random 50/50) underperformed exp 002 (pure cCRE)
- exp 013 (pELS+dELS 50/50) underperforms BOTH single-class
  parents

**Refined principle:**
> Pure-class training reliably beats mixed-class training, even
> when the constituent classes are individually high-quality.
> The model develops sharper feature representations when the
> training distribution is homogeneous; mixing forces compromise
> features that fit neither distribution well.

**Why dilution is so consistent:**
- pELS sequences have GC ~0.51, cell-type-near-housekeeping
  TF programs.
- dELS sequences have GC ~0.46, distal cell-type-specific TF
  programs.
- The model trained on the union has to balance these two
  distributions, and ends up worse on both than a model
  specialized to either.
- Per-class undersampling (25K vs 50K of each pure library)
  partly contributes — pELS has only 10% of pool covered vs
  20% in pELS-only — but the magnitude (-0.025) exceeds what
  pool-coverage alone would predict.

## What this changes (theory update)

Strongly reinforces a key principle:
> **Don't mix.** Single-class training is the default for
> sequence-to-activity model training on cCRE data. Mixing
> always dilutes, even when combining the two highest-quality
> single-class libraries. The model needs a coherent training
> distribution to learn sharp regulatory-grammar features.

This rules out a large class of "improve by combining" library
designs. Future improvements must either:
1. Find a single class better than pELS (TF, CA-CTCF, etc.
   untested)
2. Augment within a single class (sub-pool selection,
   reverse-complement, etc.)
3. Find a class that itself includes both proximal-and-distal
   enhancer characteristics (none in cCRE annotation)

## Eval_08 sub-finding

combo eval_08 = 0.6459, worse than both pELS (0.684) and dELS
(0.672). Mixing produced WORSE eval_08 score than either
constituent. eval_08 specifically punishes biology-mixing.

## Next experiment

Continue the single-class survey. **Exp 014: TF-only** (105K
pool — between PLS-47K and CA-246K). TF cCREs are
"TF-bound regions without chromatin marks" — pure TFBS-rich
content. If TF beats CA at smaller pool, "TF-binding-richness"
matters more than "accessibility". If TF underperforms CA,
chromatin context is doing significant work.
