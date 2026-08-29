# 023 — K562 motifs DENSE (16/seq) at GC=50/50

## Method
Same K562 motif panel as exp 005, but density doubled (8→16 per seq).
Both halves at GC=50.

## Results (eval_01)
mean_r = +0.0023 (K562=+0.0081, HepG2=-0.0000, SKNSH=-0.0013)

## Lesson
- K562 lifted to +0.0081 (best K562 r at GC=50, near exp 012's +0.0089).
- HepG2 collapsed to 0.0000 (was +0.0056 in exp 005 with 8 motifs).
- Dense motifs (16) destroys HepG2 signal even at GC=50.
- 8 motifs/seq is HepG2's sweet spot (some K562 motifs also broadly active).
- eval_07 = +0.0090 (record), eval_13 = +0.0038 (HepG2=+0.0101).

## Implication
- Motif density has a HEPG2 CEILING around 8-10. More breaks HepG2.
- Per-cell maxima of K562 and HepG2 are MUTUALLY EXCLUSIVE in single
  design.

## Next (exp 024)
Mild GC contrast (60/40) + exp 005's panel + 8 motifs/seq. Hypothesis:
gentle contrast lifts K562 slightly above +0.0077 without killing HepG2's
+0.0056. Target mean +0.0050.
