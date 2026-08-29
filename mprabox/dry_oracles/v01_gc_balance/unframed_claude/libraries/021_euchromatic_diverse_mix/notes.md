# 021_euchromatic_diverse_mix

7 sources × 7,150 each: chr22, chr19, chr17, chr20 (gene-dense),
whole genome, cCRE all, cCRE PLS+DNase-H3K4me3 (high GC).
Replaces chrX (weak source in 019) with chr17+chr20.

## Result
eval_01: **0.6908 — NEW BEST** (beats 019 0.6895 by +0.0013)
eval_04: 0.5968 (gain from 019's 0.5818)
eval_07: 0.7571 (small drop from 019's 0.7615)
eval_13: 0.7519 (small drop from 019's 0.7549)
GC mean=0.472 std=0.113 (narrower than 020, similar to 019)

## Interpretation
Replacing chrX with gene-dense chr17+chr20 improves eval_01 slightly.
Confirms: euchromatic real-DNA-with-variance is the winning recipe.
Multiple gene-dense chromosomes add useful variance without leaving
the predictor's training distribution.

eval_07/13 dropped slightly — they may prefer the broader chr-coverage
of 019's whole-genome+chrX. eval_04 prefers gene-dense (regulatory load).

## Next
- 022: increase cCRE PLS+DNase fraction (push high-GC variance harder)
  while keeping gene-dense base.
- Or test ratio sweeps systematically.
