# 007_whole_genome

50k random 200bp slices from all autosomes + X + Y of hg38.

## Result
eval_01: 0.6149 (vs 0.6780 chr22) — DROPPED 0.06
eval_07: 0.7595 (vs 0.7462 chr22) — best yet
eval_13: 0.7564 — best yet
eval_04: 0.3842 (vs 0.5809 chr22) — big drop
eval_08: 0.0860 (vs 0.1230 chr22) — also down

## Interpretation
Different evals prefer different genomic regions.
- eval_01, eval_04 prefer gene-rich (chr22-like) regions
- eval_07, eval_13 prefer lower-GC, more diverse (whole genome) sampling

chr22 has unusually high gene density (~600 genes in 50Mb vs ~20k in 3Gb).
Eval_01 may directly reward sequences from gene/regulatory dense regions.

Tradeoff: eval_07 vs eval_01 are pulling in opposite directions on GC/composition.
Need to find regions that maximize both — regulatory-dense AND lower GC.

## Next
- 008: PLS (promoter-like signature) only cCREs
- 009: gene-rich regions specifically (TSS-proximal)
