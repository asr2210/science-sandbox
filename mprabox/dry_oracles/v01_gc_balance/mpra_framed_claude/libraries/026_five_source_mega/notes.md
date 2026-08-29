# 026_five_source_mega

## Setup
5-source mega-pool: 10k each cCRE + ChIP + Malinois + FANTOM5 + DHS.
Tests whether adding DHS to the 4-source FANTOM5 mega-pool (exp 025)
helps or dilutes.

## Result — DHS dilutes again
- eval_01 = 0.6914 vs exp 025 0.6928 (−0.001) and exp 020 (3-source) 0.6928
- eval_04 = 0.6114 (down from exp 025 best 0.6197)
- eval_08 = 0.1270 (slightly highest)
- eval_07 = 0.7477 (down from 3-source 0.7553)

## Interpretation
Same pattern as exp 021: adding DHS as the marginal source dilutes
rather than helps. DHS is the weakest single source (exp 007 = 0.6631
alone vs 0.69 for the others), and its mixing rate above ~10% causes
small drops in eval_01.

## Theory update → T17 — DHS dilutes, FANTOM5 helps
- DHS: net negative as marginal source. Skip in best library.
- FANTOM5: net neutral on eval_01, positive on eval_04. Keep if multi-
  eval matters.
- Best recipe: 3-source (cCRE+ChIP+Malinois) for max eval_01, or
  4-source with FANTOM5 for balanced multi-eval.

## Takeaway
Final library candidate: 3-source mega-pool (~17k each) or 4-source
with FANTOM5. eval_01 saturates at 0.6928 either way; pick by
secondary criteria. Will do one more sanity test (drop Malinois) and
then finalize.
