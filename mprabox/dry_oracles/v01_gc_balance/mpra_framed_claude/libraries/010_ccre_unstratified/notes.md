# 010_ccre_unstratified

## Setup
50k cCREs sampled uniformly from full 2.35M ENCODE pool (no type
stratification). Resulting distribution (natural): 31.2k dELS, 5.3k pELS,
5.3k CA, 2.7k CA-CTCF, 2.2k TF, 1.7k CA-H3K4me3, 1.0k PLS, 0.6k CA-TF.

## Result vs exp 002 (stratified)
- eval_01: 0.6852 vs 0.6921 (−0.007)
- eval_04: 0.5727 vs 0.5977 (−0.025)
- eval_07/10/13: nearly identical (within ±0.002)
- eval_08: 0.1240 vs 0.1248 (negligible)

## Interpretation
Stratification vs unstratified gives essentially the same result. The
extra promoters / TF-evidence elements I included in stratified marginally
helped eval_04 but didn't move motif-driven evals. With or without
stratification, the cCRE library ceiling is ~0.69 on eval_01.

## Takeaway
Two months of fiddling with cCRE selection (types, augmentation, mixing,
stratification, sources) move eval_01 by <0.03. The big jump came from
random→cCRE (+0.18). To get the next 0.05 of lift I need a fundamentally
different lever — likely either:
1. Cell-type-specific MPRA training data (e.g., direct ChIP-seq for
   K562/HepG2/SKNSH key TFs)
2. A different annotation entirely (ABC enhancers, conserved CREs)
3. Information density tricks (multi-tile per cCRE — though this trades
   diversity for redundancy)
