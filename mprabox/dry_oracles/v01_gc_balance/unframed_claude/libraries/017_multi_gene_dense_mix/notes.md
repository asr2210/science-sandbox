# 017_multi_gene_dense_mix

12.5k each from chr17, chr19, chr20, chr22 (all gene-dense chromosomes).

## Result
eval_01: 0.6731 (between chr22 0.678 and chr19 0.674)
eval_07: 0.7542 — best yet for eval_07 (vs 0.7595 whole-genome)
eval_13: 0.7527 — best yet

## Interpretation
Multi-chr mix is good for eval_07/13 but doesn't beat chr22 alone for eval_01.
Confirms: cCRE-all (0.6840) is currently the best for eval_01.

## Next plan
Build on cCRE-all winning. Try filtering cCREs to balance GC composition.
