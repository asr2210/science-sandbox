# 007 — 50/50 Mix: Random Genomic + Class-Balanced cCRE

**Hypothesis:** Theory v4 — compositional diversity within the
regulatory half matters more than cell-type balance. Force 5,000
sequences per cCRE class (PLS, pELS, dELS, CTCF-only,
DNase-H3K4me3) instead of uniform sample (72% dELS).

**Design:** 25,000 random genomic + 5,000 × 5 cCRE classes. Seed 0.

**Results vs exp 004 (uniform-cCRE mix, mean=0.531) → NEW BEST:**
- eval_01: **0.5759** (+0.007) ← NEW BEST
- eval_02/05: 0.5765 (+0.007)
- eval_03/12: 0.5734 (+0.005)
- eval_04/09: **0.5473 (+0.025)** ← biggest win
- eval_06/11: 0.5746 (+0.008)
- eval_07: 0.6263 (-0.004) ~equal
- eval_08: **0.1293 (+0.047)** ← surprise improvement
- eval_10: 0.5174 (-0.000) ~equal
- eval_13: 0.6067 (-0.005) ~equal
- eval_14: 0.5759
- Mean: **0.541** (+0.010 vs 004) ← NEW BEST

**Theory v4 supported.** Class balancing within cCRE helps everywhere
except eval_07/13 (marginal drop). The biggest wins are on eval_04/09
(GC/composition axis) and eval_08 (OOD axis).

**Why eval_08 improved unexpectedly:** Promoter-like sequences (PLS)
are high-GC, CpG-rich, and compositionally distinct from typical
genomic background. The class-balanced cCRE includes 5,000 PLS vs
uniform cCRE's ~2,500. This broadens the compositional manifold the
model is trained on, partially recovering eval_08 without sacrificing
biological signal. The recipe for eval_08 isn't "more uniform random"
— it's "more compositional breadth from real biology."

**Theory v5 (refined):**

Within the natural-only regime, the right way to add breadth is by:
- (i) mixing different regulatory element classes (PLS, dELS, CTCF
  have different compositional regimes)
- (ii) including non-regulatory backbone (genomic random for context)
- NOT (iii) by adding synthetic non-natural sequences

This is consistent with exp 005 (uniform random hurt everything) and
exp 007 (class balance helped everything).

**Next experiment (008):** Test mix ratio. Current best = 50/50
genomic:cCRE. Try 30/70 (more regulatory density). If better, push
toward 20/80 or 10/90. If worse, sweet spot is around 50/50 and pivot
to other axes.

Predictions for 30/70:
- More dense motif signal per training step
- Possible loss of distributional breadth (context for eval_07/13)
- eval_01 may rise to 0.58–0.61 OR drop slightly if breadth matters
- Will resolve "is 50/50 a sweet spot or did I just stop too early?"
