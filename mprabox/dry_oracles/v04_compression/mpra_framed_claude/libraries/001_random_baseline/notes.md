# 001_random_baseline

50,000 i.i.d. uniform random 200bp ACGT sequences. Seed 42.

## Result
mean_r averaged across 14 eval sets: ~0.34
eval_01 (primary): 0.3425
Easiest: eval_07 (0.450), eval_13 (0.434), eval_10 (0.402)
Hardest: eval_08 (0.110), eval_04/09 (0.304)

## Observations
- Random sequences ALREADY give mean_r ~0.34. The model learns substantial
  structure from random-sequence/activity pairs alone — likely because random
  200bp windows contain enough motif-like k-mers by chance that simple
  k-mer→activity mappings work.
- **K562 and HepG2 always identical** across every eval set (0.338 vs 0.338,
  etc.). Either the eval is treating them as the same tissue here, or they
  happen to give identical correlations on this specific library. Watch for
  this in future experiments.
- **Eval sets come in duplicate pairs**: eval_01==eval_14, eval_02==eval_05,
  eval_03==eval_12, eval_04==eval_09, eval_06==eval_11. So there are ~9
  distinct underlying eval sets, not 14. Useful to know.
- eval_08 is dramatically harder (0.11). Likely a different kind of element —
  could be silencers, repressors, very tissue-specific, or non-canonical.

## Implications for theory
- The model can extract grammar from random data → grammar isn't the bottleneck
  at low end. The question becomes: what *additional* signal does a designed
  library provide beyond random?
- The hardest eval set (08) is where the most "informational lift" is
  possible. Future experiments should chase eval_08 in particular.
