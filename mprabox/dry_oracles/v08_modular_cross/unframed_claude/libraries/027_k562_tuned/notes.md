# 027 — K562 tuned: 14 motifs, HepG2-friendly panel adds

## Method
Exp 012 base + AGGTCA (NR), TGTTTAC (FOXA), CCAATCA. 14 motifs/seq.
GC=65 active vs GC=30 null (slightly less extreme than exp 012's 65/25).

## Results (eval_01)
mean_r = +0.0025 (K562=+0.0088, HepG2=+0.0006, SKNSH=-0.0020)

## Lesson
- K562 r essentially identical to exp 012 (+0.0088 vs +0.0089). K562
  signal robust regardless of panel tweaks.
- HepG2 STILL near 0 (+0.0006) despite adding "HepG2-friendly" motifs.
- SKNSH BROKE (-0.0020) vs exp 012's +0.0035. TGTTTAC (AT-rich) probably
  the culprit.
- eval_03 = -0.0004 but HepG2=+0.0069 — narrow win for HepG2 on one eval.

## Implication
- Panel composition has small marginal effects; K562 r capped around
  +0.0089 by some model-level constraint.
- Adding AT-rich HepG2 motifs degrades SKNSH r.

## Next (exp 028)
Re-run exp 012 EXACTLY with different seed. Test whether the +0.0045
ceiling is a hard ceiling or noisy plateau. Single-seed reproducibility
matters before declaring the plateau real.
