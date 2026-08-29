# 005 — K562-focused 50/50, matched GC=50%

## Method
25k active: GC=50% bg with 8 K562 motifs (GATA, KLF, NFE2, TAL1, AP-1,
ETS, SP1, MYB). 25k null: GC=50% no motifs.

## Results (eval_01)
mean_r=+0.0043, K562=+0.0077, HepG2=+0.0056, SKNSH=-0.0003

## Lessons
- K562_r LOWER than exp 003 (+0.0137). The GC-rich-vs-AT-null contrast
  in 003 was contributing to K562 signal, not just motif content.
- HepG2_r flipped POSITIVE (+0.0056). Confirms HepG2 model penalized
  AT-rich-null sequences in 003 (i.e., HepG2 model thinks AT-rich = active).
- SKNSH still near zero. Need SKNSH-specific motifs.

## Updated theory
- Each cell-line model has its own "active sequence" template.
- K562 model: GC-rich with K562 motifs = active. GC-rich without motifs
  is fine. AT-rich is inactive.
- HepG2 model: AT-rich with HepG2 motifs (HNF1A is AT-rich) = active.
  Plain AT-rich is also predicted relatively active.
- To maximize correlation for a cell type: I need sequences spanning
  both "definitely active" and "definitely inactive" *according to that
  cell line's biology*.
- For multi-cell maximization: I need sub-banks that are clearly
  high-activity AND clearly low-activity for each cell line.

## Best mean_r so far
- 001 random:        -0.003
- 002 GC sweep:      +0.003
- 003 motif+null:    +0.001  (K562 +0.014 dominated)
- 004 4-bank:        -0.000  (dilution killed it)
- 005 K562 50/50:    +0.004  (broader cell-line lift)

Trend: pure motif-only contrast (no GC confound) gives broader lift.
