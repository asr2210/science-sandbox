# 015_chr19_gene_dense

50k chr19 random 200bp slices. chr19 is the most gene-dense chr (~26 genes/Mb).

## Result
eval_01: 0.6741 (vs chr22: 0.6780). Slightly worse than chr22.
eval_04: 0.6105 (better than chr22's 0.581)
eval_07: 0.7316 (worse than chr22)

## Interpretation
Gene density alone doesn't push past chr22. Tied at ~0.68.

The cap is really around 0.68 for ANY real-DNA strategy I've tried.
chr22 has chr-specific advantage maybe due to its particular composition mix.

## Next
Try cCRE-all excluding PLS (which crashed by itself).
