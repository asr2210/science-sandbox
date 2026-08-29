# 020_tf_balanced_chip — notes

## Design
Exp 011 design but ChIP substitutes cCRE AND ChIP is TF-balanced
(≤30 peaks per TF, spreading across 1210 distinct TFs).

20K natural + 15K TF-balanced ChIP + 10K DHS + 5K mouse.

## Result
- eval_01 = 0.4900 (vs exp 011 = 0.5012, Δ = -0.011, ~2.7σ below)
- eval_07 = 0.5666 vs 011's 0.5946 (Δ = -0.028, significant)
- eval_13 = 0.5827 vs 011's 0.5946 (Δ = -0.012)
- Time: 22s

## Interpretation
TF balancing HURTS. Random ChIP sampling is dominated by heavily-studied
TFs (CTCF, MYC, GATA, TP53, etc.) for good reason — they ARE the
dominant regulators. Forcing equal representation of obscure TFs:
- Reduces signal density (less common motifs are less informative)
- Adds noise (low-quality peaks from rare TFs)

Eval data is dominated by activity patterns of common TFs, so a library
biased toward rare-TF motifs misses what the eval cares about.

## Implication
Don't curate atlas data for "balance" if the eval distribution is
naturally skewed. Match the eval's effective bias, not a synthetic
balance.

## Lesson summary so far (across exps 015-020)
Within-atlas curation almost always hurts:
- exp 017: PWM curation → -0.015
- exp 018: phastCons (different selection) → -0.009
- exp 019: GC stratification of natural → -0.005 (within noise)
- exp 020: TF balancing of ChIP → -0.011

Random sampling within an atlas is hard to beat. The natural skew of
biological data (rare regions are rare, common TFs dominate) matches
the eval's effective bias.

## Next test
Add a 5th source orthogonal to the 4-way mix: ChIP at small fraction
(7K) added to a slightly downsized exp 011 base. Tests if a SMALL ChIP
component (not a substitution) helps as marginal diversity.
17K nat + 13K cCRE + 8K DHS + 7K ChIP + 5K mouse = 50K.
