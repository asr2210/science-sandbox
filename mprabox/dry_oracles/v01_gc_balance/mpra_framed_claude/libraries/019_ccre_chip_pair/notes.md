# 019_ccre_chip_pair

## Setup
25k stratified cCREs + 25k ChIP-seq peaks (K562/HepG2/SKNSH 8.5/8.5/8k).
Tests whether 2-source cCRE+ChIP matches the 3-source mega-pool (018)
or is worse.

## Result
- eval_01 = 0.6913 vs mega-pool 0.6928 (−0.0015) vs cCRE-alone 0.6921 (−0.0008)
- All other evals within ±0.005 of mega-pool

## Interpretation
Slightly worse than both pure cCRE and the 3-source mega-pool. Adding
ChIP-seq to cCRE without Malinois doesn't help; if anything it
marginally dilutes cCRE signal.

The mega-pool's small win over pure cCRE was probably due to:
1. Modest 3-source diversity bonus (each source ≤ 35% of library), OR
2. Random run noise (small lift, within ~±0.001)

## Takeaway
Doesn't disprove that 018 mega-pool was a noisy win. Will run one more
variant (cCRE-heavy 30/10/10 mix) to test whether more cCRE share
beats balanced 17/17/16. If that also lands ~0.692, the ceiling is
~0.692-0.693 and we accept exp 018 as the operational winner.
