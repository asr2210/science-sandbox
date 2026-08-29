# 023 — Add 10% ReMap CRM (TF ChIP-seq consensus)

**Hypothesis:** TF ChIP-seq peaks capture actual TF binding events;
higher motif density than cCRE chromatin signatures alone should
lift eval_07/13 (motif-grounded).

**Design:** Replace 5k random genomic with 5k ReMap CRM (TFs>=50,
summit-centered, 200bp). Best base from exp 020 elsewhere.

**Results vs exp 020 (best, mean=0.5468):**
- eval_01:    0.5748 (-0.004) ← regressed primary metric
- eval_04/09: 0.5750 (+0.009) ← BIG composition lift
- eval_07:    0.6012 (-0.016) ← BIG motif drop
- eval_08:    0.2123 (+0.038) ← HUGE OOD lift
- eval_13:    0.5800 (-0.017) ← BIG motif drop
- eval_10:    0.5087 (-0.005)
- Mean:       **0.5453** (-0.0015, OUTSIDE noise!)

**Findings — SURPRISING:**

TF ChIP-seq CRMs HURT mean (-0.0015) but with a DRAMATIC tradeoff:
- LIFTS composition (+0.009) and OOD (+0.038)
- HURTS motif-grounded (-0.016/-0.017)

The eval_08 +0.038 is the biggest single-axis lift in 23 experiments.
TF CRMs are a strong OOD source. But they HURT eval_07/13 because:
1. TF CRMs are gene-proximal/active regions — overlap heavily with
   cCRE PLS class. Adding 5k more PLS-like sequences is REDUNDANT
   and crowds out cCRE diversity.
2. CRMs are 400-1000bp; 200bp summit-centered window may miss the
   broader TF binding context.
3. ReMap is biased toward K562/GM12878 ChIP-seq → over-represents one
   cell-type signature.

**Theory v6.8:** TF ChIP CRMs are an OOD source (like uniform random
and CpGi). At 10% they dilute motif learning. Try smaller dose (2.5%)
to capture the OOD benefit without the motif cost.

**Plan exp 024:** 2.5k TF CRMs (5%) displacing 2.5k random genomic.
Composition: 20k genomic + 20k cCRE multiwindow + 5k CpGi multiwindow
+ 2.5k TF CRM + 1.25k uniform + 1.25k shuffled.
