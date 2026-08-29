# 022 — Rebalanced hybrid (16.5k K562 + 8.5k HepG2)

## Method
16.5k K562 syn (GC=65, 12 motifs) + 16.5k null GC=25 + 8.5k HepG2 real
H3K27ac + 8.5k dinuc-shuf.

## Results (eval_01)
mean_r = +0.0032 (K562=+0.0058, HepG2=-0.0012, SKNSH=+0.0050)

## Lesson
- K562 lifted (0.0040→0.0058) with bigger K562 bank — confirms bank-size
  scaling.
- HepG2 went NEGATIVE despite still having an 8.5k HepG2 bank. The big
  K562 bank at GC=25 null probably looks anti-HepG2 to the model.
- SKNSH lift unexpectedly strong (+0.0050) from K562 motif spillover.
- Different evals: eval_07 = +0.0087 (HepG2 lifted +0.0123 there!).

## Implication
- Big GC contrast (65/25) on majority bank kills HepG2 even when HepG2
  bank exists. Null at GC=25 is the problem.
- Need design with NULL GC ≥ 35-40 to keep HepG2 working.

## Next (exp 023)
Go back to exp 005's "GC=50/50 K562 motifs" design but DENSER:
- 25k active: GC=50, 16 K562 motifs (vs exp 005's 8)
- 25k null: GC=50, no motifs
Hypothesis: doubling motif density on exp 005's most successful base
should lift K562 above +0.0077 while preserving HepG2 +0.0056.
Target mean +0.0055+.
