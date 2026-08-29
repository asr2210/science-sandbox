# 022_chipseq_highconf

## Setup
50k ChIP-seq peaks, selected as **top by score** (per cell type, after
200bp-bin dedup, keep highest score). K562 17k + HepG2 17k + SK-N-SH 16k.

## Result — large regression
- eval_01 = 0.6172 vs random ChIP-seq 0.6900 (**−0.073**)
- All evals down ~0.07–0.10 vs the random-ChIP exp 017

## Interpretation
Top-scoring ChIP-seq peaks are heavily concentrated at a small set of
super-bound hubs — typically housekeeping gene promoters and CTCF
boundary elements with many co-bound TFs. Selecting only those biases
the training distribution toward a narrow regulatory class (active
promoters with high TF co-binding), so the model overfits to that
class and fails to generalize to typical enhancers / less-bound
regions which dominate the eval set.

## Theory update → T14 — selection-by-quality is harmful
Three independent confirmations now that quality-metric selection
hurts:
- exp 013: top-activity Malinois → eval_01 0.4950 (vs random 0.6856)
- exp 015: top-CT-specific Malinois → eval_01 0.6600
- exp 022: top-score ChIP-seq → eval_01 0.6172 (vs random 0.6900)

The mechanism is the same in all 3: filtering on a label-correlated
metric biases the training distribution away from the eval
distribution. Models learn the bias, not the underlying grammar.

## Takeaway
Stop filtering on per-sequence metrics. Random subsampling > smart
selection (within a single source). The diversity gain comes from
**source mixing**, not within-source filtering.
