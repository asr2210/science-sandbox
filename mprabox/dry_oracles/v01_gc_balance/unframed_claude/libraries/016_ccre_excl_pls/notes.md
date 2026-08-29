# 016_ccre_excl_pls

cCREs excluding all PLS-containing categories (~1M non-PLS cCREs).

## Result
eval_01: 0.6819 (vs 0.6840 cCRE-all, vs 0.6780 chr22)
Essentially tied with cCRE-all. Marginal change.

## Interpretation
Removing PLS made very little difference because PLS were only ~8% of cCREs.
The bulk (dELS, CTCF, DNase-H3K4me3) was already dominating.

Confirms plateau at 0.68 for cCRE-based and chr22-based libraries.
