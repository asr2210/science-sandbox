# Exp 009 — Motif-dominated synthetic library

## Design
Each 200bp sequence is built by tiling 33 canonical TF motifs (5-14bp each)
back-to-back with 0-3bp random linkers. ~80% of bases come from motifs.
GC = 0.463.

## Result
**eval_01 = 0.0348 — the lowest of any library since Exp 002 dinuc.**
eval_13 = 0.022. Eval time was longer (31s vs typical 10-15s) — maybe the
model trained longer / struggled more.

## Interpretation
Motif-dominated synthetic sequences are an even WORSE training signal than
pure random uniform. The model can't generalize from "dense artificial motif
salads" to whatever the eval contains.

This is a strong informational result. It says:
- The eval distribution is **natural-DNA-like**, NOT dense-motif-like.
- Out-of-distribution training hurts even when biologically motivated.
- Within natural-DNA-distribution-like libraries, the model lands at
  eval_01 ≈ 0.04–0.05; departing from natural distribution HURTS.

## Updated principle
**Match the training distribution to the (expected) eval distribution.**
Departures in either direction (sparser motifs = uniform; denser motifs =
synthetic; high-GC = promoters; low-GC = AT-rich; etc.) all underperform
broad natural DNA sampling.

## Next step
Test if BROADER natural DNA sampling lifts performance: sample from all
24 chromosomes instead of just 3. The 0.049→0.052 gap from seeds 0 and 1
suggests the 3-chromosome sample isn't dramatically suboptimal, but more
diversity should be at least as good.

## Time
31s evaluator, 61s wall.
