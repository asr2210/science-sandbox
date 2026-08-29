# 011 — 33k strict + 17k random (strict-heavy)

## Result
- eval_01 mean=**0.8744** (K562 0.856, HepG2 0.919, SKNSH 0.848)
- vs 007 (50/50): K562 -0.006, HepG2 +0.008, SKNSH -0.014. Net -0.004.

## Interpretation
More strict → HepG2 ticks up, SK-N-SH drops, K562 stable. Net slight loss.
50/50 is near-optimum among ratios tested (R-heavy 0.867, 50/50 0.878,
S-heavy 0.874).

## Next
- 012+: hold 50/50 strict+random and try adding small third modes that lift
  SK-N-SH without hurting HepG2.
