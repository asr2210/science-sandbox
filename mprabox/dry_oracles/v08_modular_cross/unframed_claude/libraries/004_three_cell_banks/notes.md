# 004 — three cell banks + null (4-bank)

## Method
4 banks of 12,500 sequences:
- K562: GC=60%, 6 K562 motifs each (GATA1, KLF, NFE2, TAL1, AP-1)
- HepG2: GC=35%, 6 HepG2 motifs (HNF1A, HNF4A, CEBPA, FOXA, NR-half)
- SKNSH: GC=50%, 6 SKNSH motifs (ASCL1, NEUROD, CREB, POU3F2, LHX2)
- null: GC=20%, no motifs

## Results (eval_01)
mean_r=-0.0004, K562=+0.0018, HepG2=-0.0062, SKNSH=+0.0032

## Lesson
Diluting K562 motifs to 1/4 of the library KILLED the K562 signal
(+0.0137 in 003 → +0.0018 here). Other cell lines didn't compensate.

Interesting per-eval finding:
- eval_07 / eval_08 / eval_10 showed HepG2 +0.012–+0.020 with SKNSH
  −0.005 to −0.014 — these evals appear HepG2-leaning.
- eval_01, 02, 05 (the K562-leaning evals — they showed K562 jump in
  003) here gave near-zero K562 because of dilution.

## Conclusion
50/50 active-vs-null contrast beats 4-bank dilution for a single
cell type. To raise mean_r, I need EACH cell line's "active" half to
be a significant fraction of the library AND I need clearly inactive
sequences to give variance for the correlation.

## Next
Per-cell maximization experiments: 005 = K562-only 50/50 (clean motif-
only contrast at matched GC); then 006 HepG2-only; 007 SKNSH-only.
Then 008+: combine winners.
