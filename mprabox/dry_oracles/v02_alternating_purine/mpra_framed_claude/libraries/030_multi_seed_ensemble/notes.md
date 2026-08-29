# Experiment 030 — multi-seed 013 ensemble

## Design
- 7.5K uniform + 2.5K CTCF + 2.5K DNH3 from SEED=0 (12.5K positives)
- 7.5K uniform + 2.5K CTCF + 2.5K DNH3 from SEED=1 (12.5K positives)
- 25K paired far flanks total (one per positive)
- Tests if multi-seed cCRE sampling reduces variance

## Result — mean_r 0.160
- 013_seed0 = 0.166, 029_seed1 = 0.150, simple avg = 0.158
- 030 = 0.160 → slight diversity bonus on top of averaging
- eval_06/11 = 0.200 (between 013's 0.218 and 029's 0.195)
- eval_07 = 0.175 (matches 013's 0.177)
- eval_10 = 0.142 (slightly lower than both)
- eval_13 = 0.154 (matches 029's 0.150)

## Interpretation
Multi-seed ensemble works as expected: smooths between the lucky
(seed 0) and unlucky (seed 1) extremes, with a small diversity
bonus from broader cCRE coverage. NOT a new single-experiment max,
but a more ROBUST score that should generalize better.

The fact that 013_seed0 still wins on a one-shot basis (0.166)
reflects the high stochastic variance — choosing a single library
to ship would still pick 013, but 030 is the more reliable design
in expectation.

## Final theory
The 013 family design (15K uniform + 5K CTCF + 5K DNH3 + 25K
paired 1500-3000bp flanks) is the best identified pattern.
Single-experiment scores fluctuate ±0.015 from seed alone.
Robust design > lucky execution.
