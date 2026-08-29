# 001 random uniform baseline

50,000 sequences, each base i.i.d. uniform from {A,C,G,T}, seed 0.

## Result
- mean_r across 14 evals = 0.852
- eval_01 = 0.862  (primary)
- Time: 11s (very fast — eval set is small / model is small)

## Observations
- Far above prediction (predicted ~0.0–0.1).
- Eval sets pair: {01,14}, {02,05}, {03,12}, {04,09}, {06,11} returned identical
  scores. Likely ~9 unique evals plus duplicates.
- K562 noticeably weaker on eval_07 (0.78), eval_08 (0.55), eval_10 (0.69),
  eval_13 (0.77). These appear to be K562-leaning evals where motif-specific
  signal matters more than k-mer composition.
- HepG2 was almost always strong (0.85–0.91) → easier to predict by k-mer.

## Interpretation
Random uniform 200bp sequences in this MPRA must produce a wide enough
distribution of activity values that simple sequence features (GC, k-mers)
explain ~85% of population variance. The trained model picks up that mapping
and transfers it to real DNA at r≈0.86. Headroom of ~0.15 = motif/syntax-
specific signal that random data cannot teach.
