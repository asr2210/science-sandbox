# 012 — phastCons replaces genomic (not cCRE)

**Hypothesis:** Exp 011 swapped cCRE↔phastCons (same axis) and lost
ground. Try swapping genomic↔phastCons: "is evolutionarily-selected
genomic better than random genomic?" — phastCons should provide both
context AND motif info.

**Design:** 20k random genomic + 20k class-balanced cCRE (4k/class) +
5k CpGi + 5k phastCons. Same cCRE+CpGi base as exp 010, replace 5k
random genomic with 5k phastCons.

**Results vs exp 010 (best, mean=0.544):**
- eval_01:    0.5725 (-0.003)
- eval_04/09: 0.5562 (-0.008)
- eval_07:    0.6158 (+0.001)
- eval_08:    0.1691 (-0.005)
- eval_13:    0.5943 (~tied)
- eval_10:    0.5112 (~tied)
- Mean:       **0.5409** (-0.003)

**Findings:**

Slightly better than exp 011 (0.540) but still worse than exp 010
(0.544). phastCons does NOT improve over random genomic for the
"context" axis either. Two interpretations:
1. Random genomic IS the best context source — covers the full natural
   distribution (including untranscribed regions, intergenic spacing,
   etc.) that the model needs to discriminate.
2. The 5k phastCons elements I added are short conserved fragments
   centered in 200bp windows that are mostly flanking unconserved
   sequence — effectively close to random genomic but slightly biased.

**Theory v6.2:** Random genomic provides irreplaceable distributional
context. phastCons is too specific (TFBS-rich, gene-proximal) to
replace it. Adding phastCons as ADDITION (not replacement) might still
help, but at this library size budget, we're trading.

**Conclusion on phastCons:** Exhausted as a source. cCRE already
captures the regulatory grammar phastCons would add. Move on.

**Plan exp 013:** Target eval_08 (stuck at 0.17 — far below other
evals). eval_08 strongly rewards non-genomic sequences (uniform random
gives 0.58 on eval_08!). Test small uniform-random dose (5%) added
to exp 010 base: lifts eval_08 without polluting motif/composition?
