# 012_more_regulatory — notes

## Design
15K natural + 20K cCRE off-center + 10K DHS + 5K mouse.
Less natural, more cCRE than exp 011.

## Result
- eval_01 = 0.4979 (vs 0.5012 in exp 011, -0.003)
- eval_07 dropped 0.596 → 0.590 (natural backbone matters for eval_07)
- eval_04 slightly better (0.520 vs 0.518)
- eval_08 = 0.0977 (essentially unchanged)

## Interpretation
- Slight rebalance toward regulatory content (40% → 30% natural) hurts
  ~+0.003 on eval_01.
- Natural fraction of 40% (in exp 011) is near-optimal in this 4-way design.
- Don't push natural fraction below ~35%.

## Implication
The optimal ratio is near 40% natural / 40% regulatory / 10% other-natural.
Beyond that, marginal returns are tiny or negative.

## Next test
Try adding a 5th source (genuinely independent regulatory class, e.g.,
FANTOM5 enhancers from CAGE bidirectional transcription) instead of
rebalancing ratios within the existing 4 sources.
