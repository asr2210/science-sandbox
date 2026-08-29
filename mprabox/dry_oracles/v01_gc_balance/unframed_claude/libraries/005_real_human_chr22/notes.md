# 005_real_human_chr22

50k random 200bp slices from hg38 chr22 (excluded Ns).

## Result
HUGE WIN.
eval_01: 0.6780 (vs 0.4983 best synthetic; +0.21)
eval_07: 0.7462; eval_13: 0.7426 — all climbing.
eval_04: 0.5809 — recovered to near-random levels (random=0.40, so actually +0.18)
eval_08: 0.1230 — barely changed; eval_08 stays stubbornly low.

## Interpretation
Real human DNA wins across the board. The scorer rewards sequences with
real-world regulatory patterns (TF motifs, dinucleotide structure, etc.)
that random sequences lack.

Note: chr22 is GC-rich (~48%) and gene-rich but is just one chromosome.
Multi-chromosome sampling or cell-type-targeted regulatory regions should
do even better.

eval_08 is special — neither composition nor real DNA helps it. May reward
something unique (entropy? diversity?).

## Next steps
- ENCODE cCREs (candidate cis-regulatory elements) → enriched for regulatory motifs
- Cell-type-specific accessible regions (K562/HepG2/SKNSH DNase peaks)
- Multi-chromosome random sampling
