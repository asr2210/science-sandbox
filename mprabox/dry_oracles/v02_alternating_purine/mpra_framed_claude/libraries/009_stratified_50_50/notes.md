# Experiment 009 — stratified cCRE at 50/50 ratio

## Design
- 25K random genomic + 25K stratified cCRE (5K each PLS, pELS, dELS,
  CTCF, DNase-H3K4me3). GC 45.7%.

## Purpose
Isolate the stratification effect by holding random/cCRE at the
sweet-spot 50/50 (from 005). Tests whether stratification per se
helps, independent of the cCRE-vs-random ratio.

## Result — mixed; worse than 005 on average
mean_r ≈ 0.151 (vs 005's 0.156; vs 008's 0.154).

Best evals (eval_07: 0.199, best ever; eval_10: 0.148) and worst evals
(eval_06: 0.154, eval_11: 0.154 — both with K562_r = -0.02) compared to
008 (eval_06/11: 0.202 with K562_r = +0.06).

| eval | 005 | 008 | 009 |
|------|-----|-----|-----|
| 06   |0.187|0.202|0.154| **dELS-quantity matters for enhancer evals**
| 07   |0.174|0.152|0.199| **random-quantity matters for eval_07**
| 11   |0.187|0.202|0.154| (tied to 06)
| 13   |0.157|0.132|0.156|

## Interpretation
- 008 has 10K dELS vs 009's 5K dELS — eval_06/11 (enhancer-like) want
  many dELS examples.
- 008 has 10K random vs 009's 25K random — eval_07 wants random.
- **There is no single optimal library across all 14 evals**.
  Stratified 50/50 trades enhancer signal for random signal.

## Theory update (T8 → T9)
- Different eval sets reward different library compositions.
  enhancer-style evals (06/11) need lots of dELS examples; other evals
  benefit from random genomic.
- The natural cCRE distribution (dELS-dominated) accidentally
  satisfies enhancer evals well. Forced stratification reduces dELS
  count and loses enhancer signal.
- For maximum *mean* across 14 evals: keep random:cCRE ≈ 50/50,
  AND keep cCREs dELS-heavy (matching natural distribution), AND add a
  small targeted boost of PLS/CTCF for the few promoter/insulator evals.

## What to try next
Two paths:
A) Adjust the stratification weights: 25K random + 25K cCRE
   where cCRE = 15K dELS + 5K pELS + 3K PLS + 2K CTCF (keeps dELS
   dominant but adds explicit type diversity).
B) Try a *qualitatively new* design: paired cCRE+flanking, where
   each cCRE positive comes with a paired neighboring window as a
   structured negative. Tests whether informative negatives help
   over random negatives.

Going with B (paired cCRE+flank, experiment 010) because it's a
genuinely different design principle. A is just a re-weight of 008/009.
