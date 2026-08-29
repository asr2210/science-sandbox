# 016 — motif cassette (5 fixed-position JASPAR motifs)

## Design
5 consensus motifs at fixed positions (centers 30, 70, 100, 130, 170). Length-restricted to 6-14bp. Random uniform background.

## Result
- eval_01 mean_r = **0.5088** (vs random uniform 0.5177, fixed 1-motif 0.5191)
- K562 r = 0.9650 (DROP)
- HepG2 r = 0.5617
- SK-N-SH r = 0.000

## Reading
More fixed-position motifs HURT. K562 dropped 0.03 from 0.99 to 0.97. Composition drift is the cost.

Adding motifs to random uniform is a balance:
- 1 motif at fixed center (012): tiny gain
- 2 motifs Poisson random (005): no effect
- 5 fixed (016): hurts
- 6 Poisson consensus (006): hurts even more

## Implication
Motif density max ~1 per sequence. Further direction: targeted motif selection (HepG2 liver TFs) instead of more motifs.
