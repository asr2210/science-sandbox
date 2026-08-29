# Exp 024 — chr22 + 1 NF-Y (CCAAT) motif centered

50k chr22 random tiles, single NF-Y motif (5bp, strand-balanced)
placed at position 97 (center). Smallest possible motif augmentation.

## Result

| metric  | chr22 random | + 1 NF-Y centered |
|---------|-------------:|------------------:|
| eval_01 | 0.3202       | 0.3187            |
| k562    | 0.1443       | 0.1453            |
| hepg2   | 0.1990       | 0.1988            |
| sknsh   | 0.6173       | 0.6120            |

Even 1 motif slightly hurts (-0.0015). K562 +0.001 but SKNSH -0.005.
Pattern is consistent: ANY motif insertion in real DNA displaces
natural composition that the models reward.

Concluding lesson: **ZERO motif insertions** is optimal for chr22-tile
recipes. The models are calibrated to natural DNA. Engineering
in motifs cannot beat the natural state.
