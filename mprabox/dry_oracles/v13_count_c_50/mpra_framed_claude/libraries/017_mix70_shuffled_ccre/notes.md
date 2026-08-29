# Experiment 017 — DINUC-SHUFFLED cCRE supplement

## Design
Same as 013 (35k mc5 + 15k type-balanced cCREs from chr5 set) but the
cCRE sequences are dinucleotide-shuffled before inclusion. Composition
preserved per-sequence; motif identity destroyed. Sanity: 200/200 dinuc
counts match originals.

## Result vs 013 (real cCRE)
| eval | 013 (real cCRE) | 017 (shuffled cCRE) | Δ |
|------|-----------------|---------------------|---|
| 01 ★ | 0.5765 | 0.5761 | -0.0004 (noise) |
| 04 | 0.5774 | 0.5766 | -0.0008 (noise) |
| 07 | 0.6037 | 0.6024 | -0.0013 (noise) |
| 08 | 0.1730 | **0.1884** | **+0.0154** (real) |
| 10 | 0.5087 | 0.5076 | -0.0011 (noise) |
| 13 | 0.5865 | 0.5852 | -0.0013 (noise) |
| mean8 | 0.5705 | **0.5717** | +0.0012 |

## Conclusion: the cCRE supplement's value is ENTIRELY compositional
On 5 of 6 unique evals, shuffled cCREs match real cCREs within seed noise
(σ ≈ 0.001). On eval_08, shuffled cCREs *outperform* real cCREs by 0.015
(15× noise) — removing motifs actually helps the most composition-driven
eval.

Motif identity is NOT contributing to the supplement's benefit. The
30% cCRE supplement is effectively a high-GC dinucleotide enrichment.

## What is the model actually learning?
The model trained on 013 cannot be using transferable TF motif grammar
from the supplement, because the same gain comes from supplement
sequences with no real motifs. It must be using composition / k-mer
biases. This bounds the kind of "generalization" we are building: it
is shallow — based on local sequence statistics, not deep regulatory
grammar — at least for the augmentation portion.

## Surprising eval_08 gain
eval_08 is unique among the 14 (no duplicate); its scores correlate
strongly with library GC. Removing motif structure *helps* it. This
suggests eval_08 might be specifically composition-driven (k-mer / GC
prediction) and real motif structure adds correlated noise.

## Implications for next experiments
- We can substitute cheap composition-matched supplements for expensive
  cCRE curation.
- The opportunity: find a composition source that's better than cCREs
  on the *composition axis* (more uniform GC distribution, fewer extreme
  AT-rich outliers, etc.).
- Test directly: use chr19-only genomic as supplement (chr19 GC ≈ 0.48,
  highest of chr5 set, no curation cost). Should match 013/017 if
  composition is truly the mechanism.
