# Experiment 015 — soft-balanced + paired flanks (worse than 013)

## Design
- 9K dELS + 4K each of pELS/PLS/CTCF/DNH3 = 25K positives
- 25K paired flanks (1.5-3kb)

## Result — mean_r 0.154 (worse than 013's 0.166)
| eval | 013 | 015 |
|------|-----|-----|
| 06/11 |**0.218**|0.195|
| 07    |**0.177**|0.148|
| 10    |0.151    |**0.165**|
| 13    |0.126    |0.129    |
| mean  |**0.166**|0.154|

## Interpretation
Trade dELS (12K → 9K) and CTCF/DNH3 (5K → 4K each) to add PLS+pELS
boost. eval_06/11 drops because dELS lower. eval_07 drops a LOT
(-0.029) because CTCF dropped from 5K to 4K. Only eval_10 benefits.

013 is robustly the best so far. Adding PLS/pELS over-representation
doesn't help — they were not deeply under-represented in 013's natural
sample (~3K and ~600 respectively in the 15K uniform).

## Theory update (T14 → T15)
- 013's recipe (heavy dELS + 5K each of CTCF+DNH3) is the right
  positive distribution. Adding more types means cannibalizing
  the working budget.
- Need to look beyond positive distribution: maybe negative distance,
  multi-scale flanks, dinucleotide-shuffled negatives, or a new
  positive source.

## Next
016 = test negative-flank DISTANCE. 013's positives + NEAR flanks
(500-1500bp instead of 1500-3000bp). Tests if harder/closer
negatives further improve discrimination.
