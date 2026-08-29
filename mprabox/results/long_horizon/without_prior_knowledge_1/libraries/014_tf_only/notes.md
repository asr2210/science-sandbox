# 014_tf_only — notes

## Design
50K x 200bp sampled (without replacement; pool 105K) from the
TF cCRE class. Central 200-bp window. TF cCREs are TF-bound
regions (ChIP-seq) without significant chromatin marks.

## Hypothesis
TF carries pure TFBS-rich content but lacks chromatin context.
Tests "TF-binding-richness" vs "accessibility" at smaller pool
sizes. Predicted to land between PLS (47K → 0.604) and CA
(246K → 0.718) by pool-size scaling.

## Result vs. previous

| eval | rand   | dELS   | pELS   | CA     | **TF**  | Δ(TF−CA) |
|------|--------|--------|--------|--------|---------|----------|
| 01   | 0.6954 | 0.7090 | 0.7203 | 0.6775 | 0.6509  | -0.027   |
| 02   | 0.7848 | 0.8014 | 0.8129 | 0.7667 | 0.7333  | -0.033   |
| 03   | 0.7612 | 0.7897 | 0.7958 | 0.7579 | 0.7229  | -0.035   |
| 04   | 0.7494 | 0.7417 | 0.7603 | 0.7048 | 0.6793  | -0.026   |
| 05   | 0.6951 | 0.7089 | 0.7203 | 0.6777 | 0.6514  | -0.026   |
| 06   | 0.7853 | 0.8017 | 0.8133 | 0.7671 | 0.7344  | -0.033   |
| 07   | 0.6684 | 0.7605 | 0.7489 | 0.7386 | 0.7160  | -0.023   |
| 08   | 0.7841 | 0.6720 | 0.6844 | 0.6193 | 0.5401  | -0.079   |
| 09   | 0.8115 | 0.8042 | 0.8238 | 0.7638 | 0.7324  | -0.031   |
| 10   | 0.7564 | 0.7779 | 0.7729 | 0.7437 | 0.6842  | -0.060   |
| 11   | 0.6833 | 0.6973 | 0.7083 | 0.6668 | 0.6411  | -0.026   |
| 12   | 0.6553 | 0.6782 | 0.6853 | 0.6509 | 0.6227  | -0.028   |
| 13   | 0.6584 | 0.7601 | 0.7473 | 0.7441 | 0.7177  | -0.026   |
| 14   | 0.7851 | 0.8015 | 0.8129 | 0.7665 | 0.7327  | -0.033   |

Mean: rand 0.738, dELS 0.756, pELS 0.758, CA 0.718, **TF 0.683**.

## Interpretation

**TF-only sits between PLS and CA** as predicted by pool-size
scaling. Updated single-class matrix:
- PLS pool 47K → 0.604
- TF pool 105K → 0.683
- CA pool 246K → 0.718
- pELS pool 249K → 0.758
- dELS pool 1.47M → 0.756

Log-linear pool-size scaling predicts TF at 105K to score ~0.659;
actual is 0.683 (+0.024 above scaling line). TF content is
slightly more informative per element than expected from pool
size alone.

**TF underperforms CA** by -0.035 mean despite half the pool
size. Per-element-quality is comparable: TF (105K → 0.683) is
similar quality per element to CA (246K → 0.718). The chromatin
accessibility signal in CA is roughly equivalent to TF binding
content alone — neither dominates per-element.

**Big eval_08 hit:** TF eval_08 = 0.540, second worst after PLS
(0.477). TF cCREs are very biology-flavored (highly motif-rich)
which eval_08 punishes heavily. This puts TF at the
"bio-extreme" end of the eval_08 spectrum.

**Ranking of class informativeness per element (controlling for
pool size):**
- pELS-and-dELS-grade enhancer content > CA-and-TF content >
  PLS-grade narrow content.
- The factor of ~2× per-element-quality gap between
  enhancers (pELS/dELS) and accessibility-or-TF (CA/TF) is
  large.

## What this changes (theory update)

Refines the single-class hierarchy:
> Enhancer content (pELS/dELS) is intrinsically the highest-quality
> per-element training signal. Chromatin accessibility (CA) and
> TF binding (TF) carry less information per element — even
> though both are "biology" signals. Promoter-like content (PLS)
> is the worst due to narrow housekeeping grammar + tiny pool +
> extreme GC.

Combined with exp 013's strong "mixing dilutes" finding, the
playbook is becoming clear:
- Use the highest-quality single class (pELS or dELS).
- Don't mix.
- Augmenting within a single class is the only remaining lever.

## Next experiment

We've now tested 4 single classes (dELS, pELS, CA, PLS, TF — that
is, 5). Three more remain (CA-CTCF, CA-H3K4me3, CA-TF). All
smaller pools; unlikely to surprise.

Better use of next experiment: **test the mixing principle at low
fraction**. Exp 013 showed 50/50 pELS+dELS dilutes by -0.025. Does
even SMALL mixing (90/10) still dilute? Or could a small dELS
addition specifically lift the dELS-favoring evals (07, 13) without
hurting pELS's lead?

**Exp 015: 45K pELS + 5K dELS.** If mean drops below pELS-only
(0.758), the no-mix principle is iron-clad regardless of ratio.
If mean ≈ pELS-only with eval_07 and eval_13 lifted toward dELS
levels, we have a "free improvement" via small dELS spike.
