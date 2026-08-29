# Experiment 014 — asym strat + PLS boost (worse, dELS reduction dominates)

## Design
- 10K uniform cCRE + 5K PLS + 5K CTCF + 5K DNH3 + 25K paired flanks.
- Drops dELS from 013's ~12K to ~8K.

## Result — mean_r 0.151 (down from 013's 0.166)
| eval | 013 | 014 |
|------|-----|-----|
| 01   |**0.173**|0.159|
| 06   |**0.218**|0.164|
| 07   |**0.177**|0.177|
| 10   |**0.151**|0.148|
| 11   |**0.218**|0.164|
| 13   |0.126|**0.140**|
| mean |**0.166**|0.151|

Big loss on eval_06/11 (dropped 0.05). PLS boost only helped eval_13
by 0.014. Bad trade.

## Interpretation
dELS quantity is exquisitely load-bearing for eval_06/11 (and K562
enhancer signal). Drop from ~12K dELS to ~8K dELS loses the K562
enhancer pattern entirely (K562_r goes negative on eval_06/11).

## Theory update (T13 → T14)
- Cannot freely add types — dELS budget is sacred for eval_06/11.
- The 011 effect on eval_07/10/13 came from BALANCED 5-way distribution.
  013's asymmetric strat captures most of CTCF/DNH3 lift but not the
  full "balanced types" benefit.

## Next
015 = "soft balanced": all five types over-represented relative to
flanks, but dELS still leading.
- 4K PLS + 4K pELS + 9K dELS + 4K CTCF + 4K DNH3 = 25K
- 25K paired flanks
This is 011 with dELS boosted from 5K to 9K. Should keep most of
008's enhancer signal (008 had 10K dELS, got eval_06/11 = 0.20).
Tests whether balanced-with-dELS-emphasis hits a sweet spot.
