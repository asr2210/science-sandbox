# 010 — 3-Way: Genomic + class-balanced cCRE + CpG islands

**Hypothesis:** CpG islands are defined by sequence composition alone
(>50% GC and CpG obs/exp >0.6 over >200bp), distinct from cCRE PLS
which is selected from chromatin marks. Adding 5k CpG islands should
provide compositional regime diversity that lifts eval_04/09 (the
composition axis) without disrupting motif-grounded evals.

**Design:** 25k random genomic + 20k class-balanced cCRE (4k/class)
+ 5k CpG island centered (200bp around midpoint). Seed 0.

**Results vs exp 007 (50/50 genomic + cCRE-class-balanced, mean=0.541):**
- eval_01: 0.5754 (-0.0005) ~ tied
- eval_04/09: 0.5638 (+0.017) ← lift on composition axis
- eval_07: 0.6148 (-0.012) — slight drop
- eval_08: 0.1743 (+0.045) ← lift on OOD axis
- eval_13: 0.5941 (-0.013) — slight drop
- eval_10: 0.5107 (-0.007)
- Mean: **0.5439** (+0.003 vs 007) ← **NEW BEST**

**Findings:**

The CpG island addition validates that explicit high-GC compositional
regimes help BOTH eval_04/09 (composition axis) AND eval_08 (OOD axis)
even when added at just 10% of the library. Tiny tradeoffs on eval_07/13
(motif-grounded), likely because we displaced 5k cCRE.

**Theory v6 update:** Different SELECTION MECHANISMS produce
complementary distributional coverage. cCRE = chromatin marks. CpG
islands = sequence composition. Mixing both gives broader coverage
than maxing either one.

Compositional diversity is a separate axis from motif density.
Class-balanced cCRE captures motif density across regulatory types.
CpG islands capture an extreme compositional regime (high GC, CpG
density) that random genomic only covers in expectation, not by design.

**Per-cell-type pattern:** eval_04/09 lift comes from HepG2 and SKNSH
(0.565, 0.608 — strong) while K562 stays at 0.518. K562 is already
saturated on composition. The CpG island variety helps the cell types
LESS represented in cCRE training data — exactly what we want for
generalization to unseen cell types.

**Plan exp 011:** Push the "different selection mechanism" axis
further with phastCons highly conserved elements (evolutionarily
constrained). Conservation = function via natural selection, distinct
from chromatin OR composition. May add elements neither cCRE nor CpGi
captures (structured RNAs, ancient regulatory motifs).
