# 007_natural_hg38

## What
50K random 200bp windows from hg38 chr1 + chr22 (autosome + small autosome). Acceptance rate 90% (rest had N's). Realized GC mean 0.426, std 0.099.

## Why
Test whether multi-feature natural-genome variance beats single-axis synthetic.

## Results
**eval_01: 0.5408** (vs 0.4186 GC+CpG → +29%, vs 0.156 random → +247%)
- K562_r: 0.586 (vs 0.489)
- HepG2_r: 0.520 (vs 0.354)
- SKNSH_r: 0.517 (vs 0.412)

eval_07: 0.634, eval_13: 0.619 (both peaked)
eval_08: -0.039 (eval_08 is anti-correlated with naturalness — odd outlier).

## Interpretation
Natural genomic sequences have **co-correlated multi-feature variance** (GC, CpG, motifs, repeats, low-complexity, conservation) that MPRA-trained predictors agree on. Both predictors were likely trained on natural enhancer / dHS / cCRE data, so natural inputs are closest to training distribution.

eval_08 is increasingly clearly an OUTLIER — it rewards GC-uniform synthetic sequences and dislikes natural ones. May be the "out-of-distribution detector" of the set.

## Next
Try regulatory-enriched natural sequences:
- ENCODE cCREs (filtered to active regions)
- Promoter sequences around RefSeq TSS

Hypothesis: agreement is highest near MPRA-trained-on regions.
