# 007 — K562 probe (erythroid panel + universal)

**Hypothesis**: K562 will move if we focus on erythroid TFs (GATA, KLF, PU.1, NFE2 composite).

**Design**: 9-motif panel: GATA1, KLF1, GATA1-KLF1 composite (AGATAAGGCCACCC), PU.1, NFE2, AP-1, CRE, ETS, SP1. Density 6.

**Result**: eval_01 = **0.2536**. K562 = **0.131** (essentially unchanged from random 0.136). HepG2 = +0.010. SK-N-SH = 0.620.

**Interpretation**: K562 is STUCK at 0.13 regardless of motif content. Tested K562-specific motifs do not move K562_r in either direction. Either:
  - K562 model is GC-content / dinuc / global feature driven (motif-independent)
  - K562 model output is calibrated such that our 50k sequence batch has ~0.13 correlation under all motif configurations

**Implication**: stop trying to push K562 with motifs. Focus on HepG2 (most movable) and SK-N-SH (protect ceiling). May still test GC content effect on K562 once.

**Next**: Exp 008 — test 60% GC backbone with 002 motifs. If K562 jumps under high GC, GC is the K562 lever.
