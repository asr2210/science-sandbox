# 011_four_way_mix — notes

## Design
- 20K human natural
- 15K cCRE off-center
- 10K DHS summit-centered
- 5K mouse natural

## Result (41s training, 73s wall)
- **eval_01: 0.5012 — first time crossing 0.50, new best**
- Pattern: improvements on most evals over 2-way mix
- eval_08 = 0.0953 (still stuck)
- eval_13 = 0.5946 (slight gain)
- Time: 73s

## Interpretation
**The plateau breaks with multi-source diversity.** Stacking 4 sources
beats 2 sources by ~+0.006 mean_r. Source variety provides genuine
incremental signal even when individual sources are correlated (cCRE and
DHS both regulatory but slightly different).

The 5K mouse component appears to contribute on eval_13 specifically
(0.5946 vs 0.5896 in pure-human mix). Mouse is a small positive when
constrained to <10% of library.

## Hypothesis for next
With more aggressive rebalancing toward regulatory content, can we go
higher? Try:
- 15K natural / 20K cCRE off / 10K DHS / 5K mouse  (more regulatory)
OR
- Same 4-way structure but add a 5th genuinely independent source
  (e.g., promoter-TSS-centered, or conserved phastCons)
