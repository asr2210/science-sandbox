# Experiment 009: 25k full-genome + 25k cCRE-centered (mix)

## Plan
Variance test: add cCREs (likely "active") to genome random (broad). If
variance drives r, mix should beat pure genome random (0.1387).

## Result
- eval_01 mean_r = **0.1360** (K562=0.041, HepG2=0.170, SKNSH=0.197)
- Worse than genome alone (0.1387). Better than cCREs alone (0.1285).
- Score tracks **linearly with proportion of genome random content**.

## Disconfirms variance hypothesis
Adding "active" sequences does NOT boost r. The score is a per-sequence
property of the library content, not an aggregate variance metric.

## Theory update
The scorer rewards (i) real human DNA content, (ii) sequence-space coverage.
cCREs are a SUBSET of the genome (slightly different sequence distribution),
so mixing them in dilutes the "ideal" distribution.

## Next
Try chromosome-balanced sampling (each chrom equally represented) vs
length-weighted. Tests whether under-sampling small/gene-dense chroms hurts.
