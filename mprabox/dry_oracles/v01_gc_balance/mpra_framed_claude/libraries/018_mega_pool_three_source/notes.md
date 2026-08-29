# 018_mega_pool_three_source

## Setup
50k mega-pool: 17k stratified cCREs + 17k ChIP-seq peaks (K562/HepG2/
SK-N-SH balanced ~5.67k each) + 16k random Malinois oligos.

## Result — first tiny win on eval_01
- **eval_01 = 0.6928 vs cCRE-only 0.6921 (+0.0007, FIRST library to ≥ cCRE)**
- eval_03 = 0.7003 vs 0.6992 (+0.001)
- eval_04 = 0.6004 vs 0.5977 (+0.003)
- eval_07 = 0.7557 vs 0.7562 (tied)
- eval_08 = 0.1226 vs 0.1248 (−0.002)
- eval_10 = 0.6655 vs 0.6673 (tied)
- eval_13 = 0.7472 vs 0.7466 (~tied)

## Interpretation
Maximum-diversity 3-source mix lifts eval_01 by an amount comparable to
between-run noise (~+0.001). Marginally beats cCRE-alone, and trails
in nothing important. eval_04 slightly improves.

The lift is small enough that I'm not certain it's a real signal vs
seed noise — but it's the FIRST time a library has not just matched
but slightly exceeded the 0.6921 of exp 002.

## Theory update → T10
The 0.69 ceiling can budge by ~0.001 with maximum diversity, but not
substantially. This is consistent with two possibilities:
- The eval has a real intrinsic noise floor near 0.69 that's hard to
  cross
- Or there's a genuine but small benefit from cross-source diversity
  that compounds slightly when all three sources are mixed

I'll do a few more targeted experiments to see if I can push beyond
0.6928 — varying mix ratios, using high-confidence ChIP-seq, and
trying cCRE+ChIP focused mixes.

## Takeaway
New tentative winner: 018 mega-pool at 0.6928. Will iterate on this
recipe to see if any mix ratio or source-substitution variant nudges
eval_01 further.
