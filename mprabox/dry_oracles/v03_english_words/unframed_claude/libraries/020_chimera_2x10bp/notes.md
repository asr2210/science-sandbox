# Exp 020 — chimera 2× 10bp natural inserts

**Hypothesis**: If a single 10bp natural insert lifts mean_r by +0.013
(Exp 017), adding a second insert at a non-overlapping random position
should additionally boost SKNSH (if effects stack) or saturate (if
single insert already maxes the local signal).

**Result**: eval_01 = 0.4129 (-0.012 vs Exp 017, -0.011 vs random=0.4235).
SKNSH = 0.0345 — LOWER than random's 0.055!

**Interpretation**: Two inserts are worse than one. The SKNSH lift from
a single insert does NOT stack. Worse, doubling the inserts costs SKNSH
relative to random. K562/HepG2 essentially unchanged (0.587 / 0.617),
so the entire delta is on SKNSH.

**Takeaway**: The 10bp insert benefit is fragile and non-linear. Stop
multi-insert variants. Focus on tuning the SINGLE insert: length,
position, source distribution.
