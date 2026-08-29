# 001_random_baseline

50,000 uniform random 200bp sequences. Seed=42.

## Result
eval_01 mean_r = 0.4637. Most evals 0.40-0.51. eval_08 is anomalously low at 0.15.

Notable: many evals return identical values (eval_01==eval_14, eval_02==eval_05,
eval_03==eval_12, eval_04==eval_09, eval_06==eval_11). So really ~8 distinct evals.

Random sequences scoring ~0.46 Pearson is interesting — implies the scorer can extract some signal even from random. Could mean:
- "r" is correlation between two models' predictions over our library; both pick up on similar GC/dinucleotide biases.
- Or the scorer's targets are heavily driven by basic sequence stats.

Time: 9.5s scoring.
