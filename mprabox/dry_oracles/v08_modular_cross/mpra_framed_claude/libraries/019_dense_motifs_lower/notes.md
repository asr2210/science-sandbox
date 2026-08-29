# Experiment 019 — 35k motifs (5-12/seq) + 15k pELS

## What I tested
Same as 012 but LOWER motif density (5-12 inserts/seq vs 15-25).
Hypothesis: sparser motifs with more flanking context may help.

## Result — broadly worse
- eval_07: -0.0006 (vs 018's 0.0109 — sharp loss)
- eval_08: mean=0.0029, K562=0.0102 (partial recovery — K562 still hot)
- eval_10: 0.0040 (decent)
- eval_13: 0.0018
- Many evals negative
- Mean across 14 ≈ 0.0006

## What this tells me
Lower density hurts. The model needs richer co-occurrence info per
sequence. With only 5-12 motifs, sequences look more like sparse
random + a few motifs — the model can't learn rich TF combinations.

eval_08 K562 still partially fired (0.0102), suggesting the K562
signal is somewhat density-tolerant.

## Updates to theory
Confirms v3.11: density matters, and the lower bound is around 15
inserts/seq. Below that, broad coverage breaks.

## Next
Mixed-density library is the most promising direction. Combine
17.5k @ 15-25 motifs (012-style) + 17.5k @ 35-50 motifs (018-style)
+ 15k pELS. Tests whether both density regimes can coexist.
