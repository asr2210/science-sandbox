# Experiment 030 — chr19 strided non-overlapping windows

## Method
Tile chr19 with non-overlapping 200bp windows (stride 200), skip
N-containing windows, until 50K collected.

## Result
- eval_01: 0.0516

Right at the chr19 ceiling — systematic sampling doesn't beat
random sampling. Final experiment of budget.

## Summary across all 30 experiments
Best: 027_chr19_seed7 at eval_01 = 0.0519
Ceiling: 0.050 ± 0.003 across all natural-DNA chr19 variants
