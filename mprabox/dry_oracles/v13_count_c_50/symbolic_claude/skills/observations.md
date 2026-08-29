# Observations about prepare.py

## Per-experiment structure
- prepare.py reads `sequences_0.txt` (50,000 lines × 200 chars over {0,1,2,3})
- Writes `result.json` with 14 eval entries (eval_01..eval_14) and `n_seeds`, `time_s`
- Runtime ≈ 60s for one library

## Eval metric
- Each eval reports: `mean_r`, `condition_a`, `condition_b`, `condition_c`
- `mean_r = (condition_a + condition_b + condition_c) / 3` (verified on exp 001)
- The "_r" suggests Pearson r (correlation), bounded in [-1, 1]
- Random uniform yielded positive eval_01 ≈ 0.15, so there's nontrivial baseline structure

## Duplicate evals (from exp 001)
- eval_01 == eval_14
- eval_02 == eval_05
- eval_03 == eval_12
- eval_04 == eval_09
- eval_06 == eval_11
- So 14 evals → ~8 unique
- eval_07 ≈ eval_13 but not exactly equal (similar but distinct)

## Per-eval baselines from random uniform (mean_r)
- eval_01: 0.1451 (PRIMARY)
- eval_02 = eval_05: 0.1437
- eval_03 = eval_12: 0.0919
- eval_04 = eval_09: 0.4001 (high baseline)
- eval_06 = eval_11: 0.1340
- eval_07: -0.1223 (negative)
- eval_08: 0.5795 (highest baseline)
- eval_10: 0.1085
- eval_13: -0.1243 (negative)
- eval_14: 0.1451

## Critical insight (from exp 002)
- Metric is Pearson r — warning `eval/harness.py:111: ConstantInputWarning: An input array is constant; the correlation coefficient is not defined.`
- All-NaN result on a library with 4 unique strings (12500 copies each)
- condition_c sometimes returns 0 instead of NaN — different aggregation (perhaps ranks)
- So mean_r = mean(Pearson r_a, r_b, r_c) across each eval
- The arrays being correlated are length ~50000, likely (model predictions, ground truth/another model) per sequence
- To maximize: library must have HIGH per-sequence variance in whatever the predictors compute
- Identical inputs cause NaN — avoid degenerate libraries

## Strategy
- Want HIGH variance in predicted activity (so r can be high)
- Want predictors to AGREE on the rank (so r is positive)
- Diverse compositions, motifs, structure all likely contribute
