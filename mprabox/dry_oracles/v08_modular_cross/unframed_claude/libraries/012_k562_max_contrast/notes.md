# 012 — K562 max-contrast (GC65 vs GC25, 12 motifs)

## Method
25k active: GC=65% bg + 12 K562/universal motifs (overlapping placement).
25k null: GC=25% bg, no motifs.

## Results (eval_01)
mean_r=+0.0045 (new high), K562=+0.0089, HepG2=+0.0011, SKNSH=+0.0035

## Lesson
- Best eval_01 mean_r so far (+0.0045 vs prior best +0.0043).
- K562 lift modest. Plateau around +0.008-0.014.
- eval_03 K562=+0.0134 stood out.

## Next
Try TILED strong-enhancer design: dense AP-1×N tile vs poly-A null.
Universal AP-1 motif. Hypothesis: minimizing within-class variance
(near-identical active sequences) will amplify cross-class signal,
producing higher r.
