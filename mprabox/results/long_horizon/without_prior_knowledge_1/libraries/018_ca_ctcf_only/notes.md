# 018_ca_ctcf_only — notes

## Design
50K from 126K CA-CTCF cCREs (no replacement), central-200bp.
CA-CTCF = chromatin-accessible region overlapping a CTCF
binding event. Mostly insulator/boundary biology.

## Result vs. other single-class libraries

| eval | rand   | pELS012| CA011  | TF014  | CA-CTCF018 | Δ vs CA |
|------|--------|--------|--------|--------|------------|---------|
| 01   | 0.6954 | 0.7203 | 0.6775 | 0.6509 | 0.6714     | -0.006  |
| 02   | 0.7848 | 0.8129 | 0.7667 | 0.7333 | 0.7565     | -0.010  |
| 03   | 0.7612 | 0.7958 | 0.7579 | 0.7229 | 0.7473     | -0.011  |
| 04   | 0.7494 | 0.7603 | 0.7048 | 0.6793 | 0.7064     | +0.002  |
| 05   | 0.6951 | 0.7203 | 0.6777 | 0.6514 | 0.6714     | -0.006  |
| 06   | 0.7853 | 0.8133 | 0.7671 | 0.7344 | 0.7569     | -0.010  |
| 07   | 0.6684 | 0.7489 | 0.7386 | 0.7160 | 0.7289     | -0.010  |
| 08   | 0.7841 | 0.6844 | 0.6193 | 0.5401 | 0.6034     | -0.016  |
| 09   | 0.8115 | 0.8238 | 0.7638 | 0.7324 | 0.7661     | +0.002  |
| 10   | 0.7564 | 0.7729 | 0.7437 | 0.6842 | 0.7352     | -0.009  |
| 11   | 0.6833 | 0.7083 | 0.6668 | 0.6411 | 0.6604     | -0.006  |
| 12   | 0.6553 | 0.6853 | 0.6509 | 0.6227 | 0.6429     | -0.008  |
| 13   | 0.6584 | 0.7473 | 0.7441 | 0.7177 | 0.7324     | -0.012  |
| 14   | 0.7851 | 0.8129 | 0.7665 | 0.7327 | 0.7565     | -0.010  |

Mean: pELS 0.758, CA 0.718, **CA-CTCF 0.710**, TF 0.683.

## Interpretation

**Hypothesis (B) confirmed: insulator grammar is narrow.** CA-CTCF
underperforms CA (0.710 vs 0.718, Δ=-0.008) on essentially every
eval. CTCF-bound accessible regions provide LESS useful regulatory
grammar than generic accessibility, despite having a stronger and
better-defined motif (CTCF).

This is surprising at first: CTCF is one of the most studied,
strongest-binding factors. Why would CTCF-rich training hurt
generalization vs broader chromatin?

**Likely explanation:** CTCF binding is highly cell-type-invariant
(insulator/boundary biology), so a CTCF-rich library teaches the
model a feature that exists ubiquitously and provides little
discrimination across the variable regulatory landscape that
defines cell-type-specific activity. The model spends parameter
budget on CTCF when generic enhancer/accessibility grammar is
more predictive across cell contexts.

**High seed variance flag:** eval_01 = 0.642 / 0.658 / 0.715
across seeds 0/1/2 — range 0.073, ~5× typical seed variation
(usually 0.01-0.02). This suggests CA-CTCF is heterogeneous:
different 50K samples from the 126K pool produce noticeably
different models. May reflect chromatin sub-categorization
within "CA-CTCF" or position-on-chromosome sampling effects.
Worth keeping the 3-seed average but the noise is real.

## Updated single-class library matrix

| class       | pool size | mean_r | seed σ      |
|-------------|-----------|--------|-------------|
| pELS        |   249,464 | 0.758  | low         |
| dELS        | 1,469,205 | 0.756  | low         |
| CA          |   245,985 | 0.718  | low         |
| CA-CTCF     |   126,034 | 0.710  | **HIGH**    |
| TF          |   105,286 | 0.683  | low         |
| PLS         |    47,532 | 0.604  | low         |

**Hierarchy now: enhancer-like (pELS, dELS) > accessibility (CA)
> insulator (CA-CTCF) > TF-bound > promoter (PLS).** The pattern
correlates with regulatory context breadth: features that operate
across many cell types under varied conditions (enhancers) train
better-generalizing models than features that operate
ubiquitously (CTCF) or in narrow contexts (promoters).

## Theory update

**New principle: regulatory context breadth predicts library
quality.** A class is good training data when its members:
- Work in varied cell-type contexts (variable readouts)
- Have heterogeneous sequence grammar (many TF combinations)
- Are functionally complete (enhancer-like, not just markers)

CTCF binding fails the second criterion (one dominant motif).
PLS fails the first (narrow promoter context). TF-only fails
the third (binding without functional integration).

## Next experiment

**Exp 019: CA-H3K4me3 only.** 79K-element pool. CA-H3K4me3 =
chromatin-accessible region with H3K4me3 mark (active promoter
chromatin). Predicts: should perform similar to PLS (active
promoter) — i.e., worst-performing class. If it doesn't, the
"chromatin readout" framing matters more than "promoter vs
enhancer" framing.
