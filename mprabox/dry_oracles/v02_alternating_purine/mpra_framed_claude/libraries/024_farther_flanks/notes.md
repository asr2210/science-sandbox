# Experiment 024 — farther flanks (3000-6000bp)

## Design
- 013 ratio: 15K uniform + 5K CTCF + 5K DNH3 + 25K paired flanks
- ONLY change: flank distance band 3000-6000bp (was 1500-3000 in 013)

## Result — mean_r 0.150 (worse than 013's 0.166)
- eval_06/11 = 0.179 (down from 013's 0.218)
- eval_10 = 0.162 (up from 013's 0.151)
- eval_13 = 0.123 (down from 0.126)
- eval_07 = 0.153 (similar)

## Interpretation
Farther flanks WEAKEN the K562 enhancer contrast (eval_06/11 lost
0.039). The 1500-3000bp band is not arbitrary — it's the sweet spot.
At 3000-6000bp, flanks become "too random" and lose the local-context
contrast that makes them informative paired negatives.

## Next
025 = try CLOSER far flanks (1000-2000bp). Tests the other direction
of the distance sweep. If 1500-3000 is the peak, 1000-2000 should
also degrade (closer flanks may share enhancer context).
