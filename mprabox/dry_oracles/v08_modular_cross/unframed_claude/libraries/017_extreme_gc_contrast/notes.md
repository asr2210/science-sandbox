# 017 — Extreme GC contrast (70/15) + all-cell motifs

## Method
25k active: GC=70, 20 motifs from K562+HepG2+SKNSH+universal panel.
25k null: GC=15, no motifs.

## Results (eval_01)
mean_r = -0.0016 (K562=+0.0053, HepG2=-0.0018, SKNSH=-0.0081)

## Lesson
- K562 SIGNAL HELD (+0.0053, close to 012's +0.0089). Saturated motifs at
  high GC still work for K562.
- HepG2 and SKNSH went NEGATIVE. GC=15 null is probably very AT-rich,
  matching the natural HepG2 enhancer composition → HepG2 model may
  predict HIGH for null sequences (wrong direction).
- Cross-cell motif mixing also dilutes per-cell specificity.

## Implication
- Don't go below GC=25 on null when targeting HepG2.
- Mixing motifs from non-K562 cells doesn't help K562 — adds confounds.

## Next (exp 018)
Two-bank split — 12.5k pure K562 design (exp 012) + 12.5k pure SKNSH motifs
(exp 007) + 25k null at GC=40 (between exp 012's GC=25 and exp 007's
GC=50, hopefully neutral to HepG2). Adds SKNSH signal without losing K562.
