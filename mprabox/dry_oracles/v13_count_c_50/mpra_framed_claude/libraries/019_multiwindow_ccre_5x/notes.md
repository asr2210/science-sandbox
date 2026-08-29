# 019 — 5-window cCRE (4k unique × 5 offsets)

**Hypothesis:** If 2 windows/anchor beat 1, 5 windows/anchor beat 2.
Per-anchor diversity is the operative axis.

**Design:** 4k unique cCREs (800/class) × 5 windows each at offsets
{-200, -100, 0, +100, +200}bp = 20k samples.

**Results vs exp 018 (best, mean=0.5464):**
- eval_01:    0.5786 (+0.001) ← primary metric NEW HIGH
- eval_04/09: 0.5658 (-0.003)
- eval_07:    0.6173 (+0.005) ← motif lift
- eval_08:    0.1747 (-0.015) ← OOD drop
- eval_13:    0.5973 (+0.005) ← motif lift
- eval_10:    0.5138 (+0.001)
- Mean:       **0.5467** ← **NEW BEST** (+0.0003)

**Findings:**

5-window cCRE LIFTED eval_01 (primary, 0.5786 — new high) and eval_07/13
(motif-grounded). Cost: eval_08 (OOD, -0.015) and eval_04/09 (-0.003).

The dropping eval_08 makes sense: 4k unique anchors = 1/5 the cCRE
breadth → less compositional variation in cCRE-derived sequences.

Net positive but starting to see clear tradeoffs. Going from 1→2→5
windows: each step gave smaller mean gain. Diminishing returns.

**Theory v6.7 confirmed:** Per-anchor diversity matters; the curve is
positive but with diminishing returns. Probably nothing to gain from
7+ windows.

**Plan exp 020:** Apply multi-windowing to CpGi too. CpGi currently
5k anchors × 1 window each. Try 1k unique × 5 windows. If the
windowing principle generalizes across sources, this lifts.
