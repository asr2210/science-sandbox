# 013 — 25k strict + 25k (random + 2 SK-N-SH motifs)

## Result
- eval_01 mean=**0.8759** (K562 0.847, HepG2 0.912, **SKNSH 0.869**)
- Compared to 012 (1 motif): SK-N-SH dropped from 0.878 to 0.869, K562 from
  0.852 to 0.847. HepG2 ticked up.
- Compared to 007 (0 motifs): worse on mean.

## Interpretation
SK-N-SH motif lift **saturates at 1 motif per random seq**. More motif is
counterproductive — either composition drifts too far or the motif crowding
disrupts the per-seq signal. 012's recipe is the local maximum on this axis.

## Next
- 014: replace SK-N-SH with K562 motif (1 per random) — does K562 also lift?
- If yes, 015 = combine both at 1+1 dose.
