# 021 — Hybrid: K562 synthetic + HepG2 real H3K27ac

## Method
- 12.5k K562 syn active (GC=65, 12 K562 motifs) + 12.5k null (GC=25)
- 12.5k HepG2 real H3K27ac peaks + 12.5k dinuc-shuffled
Each cell's predictor sees its own 50/50 split.

## Results (eval_01)
mean_r = +0.0038 (K562=+0.0040, HepG2=+0.0034, SKNSH=+0.0039)

## Lesson
- FIRST DESIGN WITH ALL 3 CELLS POSITIVE on eval_01!
- mean barely below exp 012's +0.0045, but BALANCED.
- K562 r dropped from 0.0089→0.0040 (halved bank size, halved signal).
- HepG2 r ≈ 0.0034 (down from 0.0069 in exp 015 — same effect).
- SKNSH inadvertently lifted by K562 motifs (universal-ish panel) AND
  HepG2 peaks (some shared neuronal TFs).
- eval_08 = +0.0080 (SKNSH=+0.0154), eval_07 = +0.0054 (K562=+0.0119).

## Implication
- Combining bank designs gives BALANCED per-cell lift but DILUTED.
- Net mean: hybrid (+0.0038) < pure K562 (+0.0045).
- BUT: with the right cell balance, hybrid could beat pure K562.
- Possible recipe: bias toward larger K562 bank since K562 contributes
  most variance per bank-size.

## Next (exp 022)
Reweight: 16.5k K562 syn active + 16.5k null + 8.5k HepG2 real active +
8.5k HepG2 dinuc-shuffled. More K562 budget → push K562 r toward +0.0060
while keeping HepG2 around +0.0025. Target mean +0.0050.
