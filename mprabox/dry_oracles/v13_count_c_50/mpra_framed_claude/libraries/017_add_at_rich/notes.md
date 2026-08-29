# 017 — Add 5% AT-rich genomic (low-GC tail)

**Hypothesis:** Symmetric compositional coverage. CpGi covered high-GC
tail; AT-rich (GC<0.35) should cover low-GC tail.

**Design:** Extend exp 016 base. 20k genomic + 20k cCRE + 5k CpGi +
2.5k AT-rich + 1.25k uniform + 1.25k mono-shuffled.

**Results vs exp 016 (best, mean=0.5460):**
- eval_01:    0.5741 (-0.002)
- eval_04/09: 0.5562 (-0.014) ← composition HURT
- eval_07:    0.6164 (+0.007)
- eval_08:    0.1735 (-0.026) ← OOD HURT
- eval_13:    0.5948 (+0.007)
- eval_10:    0.5125 (+0.001)
- Mean:       **0.5423** (-0.004)

**Findings:**

AT-rich windows HURT the composition axis. Likely reasons:
1. AT-rich regions are already abundant in random genomic (most non-
   coding DNA is AT-rich). The natural distribution already covers
   low-GC well; explicit oversampling adds nothing new.
2. AT-rich genomic windows are biased toward low-complexity / repetitive
   regions (heterochromatin, satellite DNA, LINE-1) which have weird
   MPRA characteristics and may pull the model in bad directions.

**Theory v6.6:** Adding compositional regimes that are ALREADY
abundant in random genomic doesn't help — only UNDER-represented
regimes help. CpGi (high-GC, ~5% of genome) was under-represented and
helped. AT-rich (~50% of genome) is over-represented and hurts.

**Plan exp 018:** Switch axes entirely. Try multi-window cCRE
augmentation — same cCREs but with 2 different windows (mid and
mid+100bp). Tests "is per-anchor diversity better than per-anchor
breadth?" Easy to implement, no new data.
