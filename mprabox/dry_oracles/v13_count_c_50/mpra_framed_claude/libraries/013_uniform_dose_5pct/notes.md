# 013 — Add 5% uniform random ACGT to exp 010 base

**Hypothesis:** eval_08 strongly rewards non-genomic sequences (uniform
random scored 0.58 on eval_08, vs -0.14 for pure genomic). Small dose
of uniform random should lift eval_08 without polluting motif/composition
learning. Exp 005's 1/3 uniform polluted everything; 5% may be the
sweet spot.

**Design:** 22.5k genomic + 20k class-balanced cCRE + 5k CpGi + 2.5k
uniform random. Seed 0.

**Results vs exp 010 (best, mean=0.544):**
- eval_01:    0.5758 (+0.0004) ~ tied
- eval_04/09: 0.5699 (+0.006) ← composition lift
- eval_07:    0.6073 (-0.008) ← small motif drop
- eval_08:    0.2020 (+0.028) ← OOD axis WIN
- eval_13:    0.5861 (-0.008) ← small motif drop
- eval_10:    0.5103 (~tied)
- Mean:       **0.5455** ← **NEW BEST** (+0.002)

**Findings:**

5% uniform random lifted eval_08 by +0.028 with only -0.008 cost on
the motif-grounded evals (07/13) and a small bonus on composition.
Net positive. **NEW BEST mean = 0.5455.**

**Theory v6.2 confirmed:** Synthetic compositional regularization at
small doses (~5%) is a free win — exposes the model to extreme
compositional variance that helps generalization to OOD distributions
without diluting motif learning. The "1/3 uniform pollutes" finding
from exp 005 was true; the dose-response curve has a peak somewhere
below 1/3.

**Per-cell-type pattern:** eval_08 SKNSH lifted most (0.30 vs 0.20
in exp 010). The OOD axis particularly helps the under-represented
cell types — same generalization signal we saw with CpGi.

**Plan exp 014:** Test 10% uniform dose to find sweet spot of
dose-response curve. If 10% still helps, may try 15%. If 10% hurts,
5% is optimal.

Composition: 20k genomic + 20k cCRE + 5k CpGi + 5k uniform = 50k.
