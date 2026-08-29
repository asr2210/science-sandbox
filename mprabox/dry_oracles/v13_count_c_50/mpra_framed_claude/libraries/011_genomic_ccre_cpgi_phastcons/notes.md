# 011 — 4-Way: Genomic + cCRE + CpGi + phastCons (substituting cCRE)

**Hypothesis:** phastCons highly conserved elements (evolution-based
selection) provide complementary info beyond chromatin marks (cCRE)
and sequence composition (CpGi). Theory v6 predicts adding a 4th
distinct selection mechanism lifts mean.

**Design:** 25k genomic + 15k class-balanced cCRE (3k/class) + 5k CpGi
+ 5k phastCons (length>=50, LOD>=50, centered 200bp). Substituted 5k
cCRE → 5k phastCons relative to exp 010 (current best, mean=0.544).

**Results vs exp 010 (best, mean=0.544):**
- eval_01:    0.5736 (-0.002) ~ tied
- eval_04/09: 0.5487 (-0.015) ← regressed on composition
- eval_07:    0.6247 (+0.010) ← lift on motif-grounded
- eval_08:    0.1349 (-0.040) ← regressed on OOD
- eval_13:    0.6040 (+0.010) ← lift on motif-grounded
- eval_10:    0.5133 (+0.003)
- Mean:       **0.5398** (-0.004)

**Findings:**

phastCons gave a clean **tradeoff** rather than a net win:
- LIFTS motif-grounded evals (eval_07/13): conserved elements ARE
  motif-rich (TF binding sites preserved by purifying selection)
- HURTS composition (eval_04/09) and OOD (eval_08): phastCons sequences
  are skewed toward coding-adjacent regions, not compositionally exotic

**Implication for theory v6:** Selection mechanisms are NOT all equally
complementary. phastCons overlaps cCRE territory (TF binding sites)
more than it overlaps CpGi territory (high-GC compositional regime).
We swapped cCRE→phastCons and got a flavor shift within "motif-rich
regulatory", not a new dimension.

**Theory v6.1:** The axes are:
- Compositional regime (random genomic, CpGi)
- Regulatory motif density (cCRE classes, phastCons)
- OOD/exotic (eval_08 specific)
Mixing complementary AXES helps. Mixing within an axis doesn't.

**Critical insight:** This was a SUBSTITUTION not an ADDITION. To test
if phastCons adds value, we need to ADD it without removing cCRE.

**Plan exp 012:** Replace 5k random genomic (not cCRE) with 5k
phastCons. Keeps exp 010's cCRE+CpGi advantage intact but turns 5k
"unselected genomic" into "evolutionarily selected genomic". If
conservation contains more info than raw context, this lifts. If
context (random genomic) is what helps eval_07/13/01, this hurts.
