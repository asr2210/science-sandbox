# Experiment 022 — paired flanks + random (worse than 013)

## Design
- 25K positives (013 ratio) + 12.5K paired far flanks + 12.5K random

## Result — mean_r 0.153
- eval_06/11 = 0.204 (down from 013's 0.218)
- eval_10 = 0.111 (very bad)
- eval_13 = 0.135 (slight lift over 013's 0.126)

Same pattern as 012, 019: any random-negative dilution hurts net mean.

## Next
023 = explore positive sub-class: dELS-CTCF-bound (278K available)
as a boosted positive type. Tests if CTCF-bound enhancers
discriminate differently than pure dELS.
