# Exp 021 — chimera 10bp natural insert at FIXED center

**Hypothesis**: Maybe the SKNSH model has a positional bias; placing the
insert at center (position 95..104) might enhance or hurt.

**Result**: eval_01 = 0.4186 (-0.006 vs Exp 017's 0.4248).
SKNSH = 0.0435 (vs 0.06 in random-position Exp 017).

**Interpretation**: Fixed center position is WORSE than random position.
The benefit of natural inserts depends on positional diversity. Plausible
reason: when all 50k sequences have the insert at the same position, the
correlation across sequences is dominated by the random scaffold at non-
insert positions (which is now 190bp instead of 200bp), reducing variance.

**Takeaway**: Keep insert positions random. Position diversity adds
useful variance.
