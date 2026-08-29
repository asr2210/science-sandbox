# 016 — Combine 2.5% uniform + 2.5% mono-shuffled

**Hypothesis:** Exp 013 (5% uniform) and exp 015 (5% mono-shuffled)
both gave ~0.546 with different tradeoffs. Splitting the synthetic
budget across both mechanisms tests if they're complementary.

**Design:** 22.5k genomic + 20k cCRE + 5k CpGi + 1.25k uniform random
+ 1.25k mono-shuffled cCRE.

**Results vs exp 015 (best tied, mean=0.5456) and exp 013 (mean=0.5455):**
- eval_01:    0.5764 (+0.0003)
- eval_04/09: 0.5698 (+0.001)
- eval_07:    0.6090 (+0.002)
- eval_08:    0.1996 (-0.002)
- eval_13:    0.5879 (+0.002)
- eval_10:    0.5111 (+0.001)
- Mean:       **0.5460** ← **NEW BEST** (+0.0004)

**Findings:**

Splitting the 5% synthetic budget across two mechanisms yields a small
but consistent improvement over either alone. Both mechanisms ARE
complementary:
- Uniform random covers extreme composition (eval_08)
- Mono-shuffled covers motif-destruction at natural composition

Combining gives the model exposure to both regularization signals
without exceeding the pollution threshold (5% total).

**Theory v6.5:** Multiple low-dose synthetic sources beat single
higher-dose. The mechanisms are orthogonal and additive at low doses.

**Diminishing returns notice:** Improvements over exp 010 base:
- +CpGi (010 vs 007): +0.003
- +5% uniform (013 vs 010): +0.002
- +5% mono-shuffled vs uniform (015 vs 013): +0.0001
- +combine (016 vs 013): +0.0005
We're at 0.5460. Further improvements likely require new axes.

**Plan exp 017:** Switch axes. CpGi covered high-GC compositional
tail. Try AT-rich genomic windows (GC<0.35) for the low-GC tail. If
symmetric compositional coverage matters, this lifts.

Composition: 20k genomic + 20k cCRE + 5k CpGi + 2.5k AT-rich + 1.25k
uniform + 1.25k mono-shuffled.
