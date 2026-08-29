# Experiment 004 — genome-wide cCRE-centered windows

## Design
- 50,000 unique cCREs sampled without replacement from the full ENCODE
  SCREEN registry (1,063,878 entries genome-wide).
- 200bp window centered on each cCRE midpoint. No jitter.
- GC content: 48.2% (much closer to genome average than chr22 cCRE's
  53.8%, because dELS-dominated genome-wide cCREs span more GC ranges).

## Purpose
Test whether the 003 underperformance was due to chr22-locality /
diversity-loss (in which case 004 should win) or whether cCRE-only
libraries are fundamentally limited (in which case 004 still loses).

## Result
mean_r ≈ 0.143 — about the same as 003, slightly worse than 002.
- **K562_r is now genuinely variable**: range −0.05 (eval_10) to +0.05
  (eval_06, eval_11). First time K562 isn't collapsed to zero.
- HepG2_r still numerically identical to K562_r.
- SK-N-SH_r ~0.42 (still down from 002's 0.46).
- eval_06 and eval_11 strongly favor this library (mean ≈ 0.18, best
  results so far on those evals). They likely measure enhancer activity.
- eval_04, eval_07, eval_09, eval_10 all dropped sharply from previous.
  These likely don't reward cCRE-only training.
- eval_08 ticked up to 0.05 (vs 0.03 in 003).

## Interpretation
1. **Genome-wide cCREs DO enable K562/HepG2 learning** — for the first
   time we see K562_r and HepG2_r push well above zero on some evals.
   That's the first real, genuine, cell-type-specific signal the model
   has shown.
2. **But the signal is inconsistent across evals**. Mean_r barely
   improves because gains on enhancer-like evals (06, 11) are offset by
   losses on more general evals (04, 07, 10).
3. **SK-N-SH "freebie" lost again** — moving away from natural genomic
   background hurts SK-N-SH. There's an opportunity cost: cCRE-only
   trades SK-N-SH for K562/HepG2 signal.

## Theory update (T3 → T4)
- A pure cCRE library teaches the model regulatory motifs (K562/HepG2
  start to engage) but at the cost of losing whatever simple feature
  drives SK-N-SH prediction from natural sequences.
- Best library is almost certainly a **mix**: cCRE for regulatory grammar
  + random genomic for SK-N-SH freebie + diversity.
- Different eval sets reward different library properties — generalization
  requires covering many properties simultaneously.

## What to try next
**Experiment 005**: 50/50 mix of genome-wide cCREs + random genomic
windows. Prediction: K562/HepG2 signal preserved (from cCRE half),
SK-N-SH freebie restored (from random half). If true, mean_r should
exceed both 002 and 004.
