# 030_final_compound_regulatory

FINAL experiment. 028 winning recipe + add 5k cCRE dELS,CTCF-bound
(compound regulatory: distal enhancer + CTCF) at cost of cCRE_all.

## Result
eval_01: 0.6940 — TIES 028 exactly (within noise)
eval_07: 0.7476
eval_13: 0.7393
GC mean=0.484 std=0.112

## Interpretation
dELS,CTCF-bound addition was neutral. The library has saturated the
"composition-driven" signal the scorer rewards.

## Final landscape
Ties for best: 028 and 030 at 0.6940.
The winning recipe: ~50% chr-derived (gene-dense + WG) + ~30% TSS-proximal
high-GC cCRE (PLS+DNase-H3K4me3+pELS) + ~10-20% cCRE_all.

The ceiling near 0.694 likely reflects the fundamental agreement between
the scorer's predictor and ground-truth models on a maximally diverse
library of real regulatory + genomic DNA. To push higher would likely
require sequences from the predictor's actual MPRA training distribution.
