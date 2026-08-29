# 004 — 50/50 Mix: Random Genomic + cCRE

**Hypothesis:** Theory v3 (c) — distributional breadth + motif density
together > either alone. 50% random genomic (breadth) + 50% cCRE
(density). Predicted eval_01 ≈ 0.55–0.57.

**Design:** 25,000 random genomic + 25,000 cCRE-centered. Mixed and
shuffled. Seed 0.

**Results (mean_r per eval, Δ vs exp 002 / exp 003):**
- eval_01: **0.5687** (+0.065 / +0.054) — BIGGEST PRIMARY GAIN YET
- eval_02/05: 0.5694 (+0.064)
- eval_03/12: 0.5684 (+0.049)
- eval_04/09: 0.5218 (vs 0.387 / 0.553) — kept most cCRE gain
- eval_06/11: 0.5671 (+0.062)
- eval_07: 0.6303 (vs 0.637 / 0.481) — RECOVERED from cCRE damage
- eval_08: 0.0818 (vs -0.136 / 0.305) — partial only
- eval_10: 0.5177 (+0.062)
- eval_13: 0.6115 (vs 0.621 / 0.466) — RECOVERED
- eval_14: 0.5687
- Mean across 14: **0.531** (vs 0.458 / 0.493) — best yet
- Time: 32 s

**Per-cell-type for previously-affected evals:**
- eval_07: K562 0.70, HepG2 0.60, SKNSH 0.59 — all back near genomic levels
- eval_13: same pattern, fully recovered
- eval_04/09 K562: 0.45 (lower than cCRE 0.51) — the K562 over-fit from cCRE was diluted

**Theory v3 — strongly supported:**

Mixing > either pure. eval_07/13 recovered without losing eval_04/09
benefits. eval_08 partially recovered but is still the worst eval.

**What's left:**

1. eval_08 still at +0.08. This eval rewards non-genomic distribution
   exposure — exp 001 (random uniform) scored 0.58 on it but exp 003
   (cCRE) only got 0.31. Adding a fraction of *random uniform*
   sequences may push eval_08 up substantially without hurting the
   genomic+cCRE mix on other evals.

2. eval_04/09 is at 0.52 — about halfway between cCRE (0.55) and
   genomic (0.39). To push higher, may need explicit GC-distributed
   sequences.

3. K562 vs HepG2 vs SK-N-SH balance is more even in mixed than in
   cCRE — confirming that cCRE bias was hurting HepG2/SKNSH.

**Next experiment:** 3-way mix — 1/3 random uniform + 1/3 random
genomic + 1/3 cCRE. Direct test of theory v3 (c+d): maximum
distributional breadth.

Predictions:
- eval_08 lifts to 0.20–0.35 (toward what 001 achieved without
  losing what 003 achieved)
- eval_07/13 stay around 0.60+
- eval_01 stays around 0.55 or marginally drops
- Mean stays around 0.53 or improves
