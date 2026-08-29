# Exp 003 — Dense cocktail (16 inserts/seq)

Same motif palette as exp 002, doubled inserts per sequence.

## Result

| metric  | exp 001 | exp 002 | exp 003 |
|---------|--------:|--------:|--------:|
| eval_01 | 0.2307  | 0.2541  | 0.2063  |
| k562    | 0.1361  | 0.1262  | 0.0553  |
| hepg2   | -0.0742 | 0.0186  | 0.0109  |
| sknsh   | 0.6302  | 0.6174  | 0.5528  |

Density backfires. K562 (-0.07) and SK-N-SH (-0.06) take real hits;
HepG2 barely changes. Suggests: the score is NOT a monotonic function
of "motif content". The model rewards naturalistic enhancer-like
sequences with moderate motif density, not heavily tiled motifs.
