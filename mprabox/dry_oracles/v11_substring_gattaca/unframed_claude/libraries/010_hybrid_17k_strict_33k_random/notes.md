# 010 — 17k strict + 33k random (random-heavy)

## Result
- eval_01 mean=**0.8673** (K562 0.842, HepG2 0.891, SKNSH 0.868)
- vs 007 (50/50): mean 0.878. K562 -0.020, HepG2 -0.020, SKNSH +0.006.

## Interpretation
More random → SK-N-SH ticks up slightly, K562/HepG2 drop noticeably. Net
loss. Ratio sweep: 50/50 better than random-heavy.

## Next
- 011: strict-heavy ratio (2/3 strict + 1/3 random) bracketing.
