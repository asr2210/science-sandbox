# Experiment 021 — 30K positives + 20K flanks (3:2 ratio)

## Design
- 18K uniform + 6K CTCF + 6K DNH3 (013 ratio scaled 1.2x) = 30K
- 20K far paired flanks (each of first 20K positives gets one)

## Result — mean_r 0.157 (worse than 013)
- eval_06/11 = 0.211 (close to 013's 0.218)
- eval_10 = 0.116 (WORST of any 013-variant)
- eval_13 = 0.132 (similar to 013's 0.126)

## Interpretation
50/50 positive:flank ratio is the sweet spot. More positives + fewer
flanks loses eval_10/13 — those evals need every positive to have a
paired flank for the geographic-context signal.

## Next
022 = mix paired flanks + random as negatives. Tests if a small
random component recovers eval_13 without losing too much eval_06/11.
- 25K positives (013 ratio) + 12.5K paired flanks + 12.5K random.
