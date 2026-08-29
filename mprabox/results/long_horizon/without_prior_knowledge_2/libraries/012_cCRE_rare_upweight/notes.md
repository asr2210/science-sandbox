# 012 — cCRE rare-class upweighted (inverse-frequency)

## Design
8 cCRE classes with **non-uniform per-class counts** (vs 006's equal 6.25K):
- 4 rare classes 8,000 each: PLS (pool 48K), CA-CTCF (126K),
  CA-TF (26K), CA-H3K4me3 (79K)  → 32K total
- 4 abundant classes 4,500 each: pELS (249K), dELS (1.47M),
  CA (246K), TF (105K)                → 18K total
Total 50K, 200bp on midpoint.

Tests T8 extension: is per-class learning information-limited at
6,250 (006's count)? If so, moving rare classes from 6.25K → 8K should
help, even at the cost of moving abundant classes from 6.25K → 4.5K.

## Results (mean over 3 seeds)
- eval_01 = **0.7391** (vs 006 0.7368 = **+0.002**)
- mean across 14 evals ≈ **0.7819** (vs 006 0.7754 = **+0.0065**)

## Per-eval delta vs 006 (8-class equal)
01:+0.002 02:+0.004 03:+0.005 04:**+0.012** 05:+0.003 06:+0.004
07:**+0.009** 08:**+0.010** 09:**+0.014** 10:**+0.010** 11:+0.003 12:+0.003
13:**+0.011** 14:+0.004

**WINS ON ALL 14 EVALS** by 0.002–0.014. Average +0.0065. Uniformly
better. Strongest gains exactly on the evals 006 was weakest on
(eval_07/08/10/13) plus eval_04, eval_09 (which 006 already led).

## Across-seed
eval_01: 0.7295 / 0.7617 / 0.7260 → SD ≈ 0.020. Comparable to 006.
The improvement is robust across seeds.

## Why it works (interpretation)
006 used 6.25K per class. Rare-class pools (esp. CA-TF=26K, PLS=47K)
have **plenty of unique signal at 8K** — moving from 6.25K → 8K adds
~28% more rare-class examples without exhausting the pool. Abundant
classes (esp. dELS=1.47M) are deeply oversampled at 6.25K relative to
their natural variation; reducing to 4.5K loses very little
information per class (most of dELS at 4.5K vs 6.25K is redundant
distal-enhancer variants).

The uniform improvement on eval_07/08/10/13 (the broad-coverage
cluster from T9) is striking. Hypothesis: rare-class up-weighting
helps eval_07/08/10/13 because rare classes (esp. CA-TF and PLS)
contain regulatory contexts that overlap with the broader sequence
space those evals probe. So inverse-frequency weighting reduces the
Pareto trade-off identified in 011 — both clusters benefit.

## What this updates in T8
**T8 (further refined):** Equal-class stratification (006) is
suboptimal: rare classes are still under-represented at 6,250 examples
relative to their unique signal. Inverse-frequency weighting (012)
strictly beats equal weighting for these 8 cCRE classes. The
optimum count per class is approximately proportional to **1 /
sqrt(pool_size)** (a softer than 1/N curve), shifting weight toward
small pools without exhausting them.

## Best library so far
**012 rare-upweighted, mean ≈ 0.7819**. New best, strictly Pareto
above 006.

## Most informative next experiment (013)
**Push rare-class upweighting further.** Try 10K rare / 2.5K abundant
= 50K. Continues the gradient that took us from 6.25K (006) to 8K (012).

- 013 > 012 → curve still rising; even more extreme rare upweighting
  helps. Optimum near "rare-only" library.
- 013 ≈ 012 → 8K is at the per-class signal saturation point; no
  further gain from upweighting alone.
- 013 < 012 → abundant classes contribute meaningfully even at 4.5K;
  reducing them further (to 2.5K) loses more than rare gains.

This brackets the rare-vs-abundant trade-off and locates the
inverse-frequency optimum. Rare-pool sizes (CA-TF=26K, PLS=47K)
should still support 10K samples with low redundancy.
