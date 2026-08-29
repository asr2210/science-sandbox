# Experiment 019: Kitchen-sink 5-source combination

## Design
- 10.2K cCRE-DNase intersection (3.4K each cell)
- 15K pure cCREs (broad regulatory)
- 15K DNase (5K each cell)
- 5.1K CTCF ChIP (1.7K each cell)
- 5K random
= 50K. Seed=19.

## Results — strong upper band
eval_01 = **0.0765** (K562=**0.0809**, HepG2=**0.0813**, SKNSH=0.0674)

| eval | 009 | 019 |
|---|---|---|
| 01 mean | 0.0772 | 0.0765 |
| 01 K562 | 0.0799 | 0.0809 |
| 01 HepG2 | 0.0812 | 0.0813 |
| 01 SKNSH | 0.0705 | 0.0674 |
| 03 | 0.0955 | 0.0951 |
| 04 | 0.0913 | 0.0906 |
| 06 | 0.0765 | 0.0767 |
| 07 | 0.1437 | 0.1429 |

K562 and HepG2 per-cell at new highs (within noise). SKNSH still weak.

## What I learned
**Even maximum source diversity tops out at the same band.**
The kitchen-sink design (5 different signal sources combined) gives
eval_01 = 0.0765 — within noise of 009's 0.0772 and well within the
established band 0.072-0.078.

K562 and HepG2 hit fresh per-cell highs (0.081), consistent with the
intersection signal (017) and the rich source mix. SKNSH (0.0674) is
again the limiter — its ceiling appears to be intrinsic, not data-dependent.

## Plateau confirmed
After 17 distinct designs spanning composition tweaks, augmentation,
quality filtering, intersection, multi-cell, and qualitatively-new
signals (CTCF), every design lands in eval_01 [0.072, 0.078]. The
ceiling is in the model/pipeline.

## Final strategy
Use remaining ~11 experiments for:
- One untried compositional axis (exp 020: all-classes cCRE)
- Multi-seed validation of leading designs (009 and 019)
- Final consolidation experiment if any clear winner emerges
