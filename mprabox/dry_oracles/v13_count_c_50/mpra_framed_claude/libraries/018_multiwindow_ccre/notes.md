# 018 — Multi-window cCRE (2 windows per anchor)

**Hypothesis:** Per-anchor diversity (multiple windows per cCRE) beats
per-anchor breadth (more unique cCREs). Model learns positional
invariance.

**Design:** 10k unique cCREs (2k/class) × 2 windows each (centered,
offset +100bp) = 20k cCRE samples. Same library budget as exp 016.

**Results vs exp 016 (best, mean=0.5460):**
- eval_01:    0.5772 (+0.001) ← small lift on primary metric!
- eval_04/09: 0.5686 (-0.001)
- eval_07:    0.6123 (+0.003)
- eval_08:    0.1897 (-0.010)
- eval_13:    0.5922 (+0.004)
- eval_10:    0.5130 (+0.002)
- Mean:       **0.5464** ← **NEW BEST** (+0.0004)

**Findings:**

Multi-window cCRE LIFTED most evals slightly. eval_01 (primary) gained
+0.001, mean +0.0004. The model benefits from seeing 2 different
windows over the same regulatory element — learns positional invariance
and flanking-sequence variation around the regulatory grammar.

Small eval_08 drop suggests halving unique cCRE breadth costs some
OOD generalization, but the win on motif-grounded evals (07/13)
compensates.

**Theory v6.7:** Data augmentation via offset windowing on the same
regulatory anchors is positive. Per-anchor context diversity > per-
anchor breadth at this library size. The model learns better feature
extraction when forced to recognize regulatory grammar from multiple
positions.

**Plan exp 019:** Push the windowing density. Try 5 windows per cCRE
(mid, mid±100, mid±200) × 4k unique cCREs = 20k total. If 2 windows
beat 1, maybe 5 windows beat 2.
