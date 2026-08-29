# 020 — Universal-only saturated bimodal (GC60 vs GC30)

## Method
25k active: GC=60, 16 universal motifs (AP-1, SP1, ETS, CREB, NF-Y, MYC,
generic E-box, NR half-site). 25k null: GC=30.

## Results (eval_01)
mean_r = -0.0028 (K562=-0.0066, HepG2=-0.0029, SKNSH=+0.0011)

## Lesson
- K562 BROKE (-0.0066) without K562-specific motifs (GATA1, KLF1, TAL1).
- Universal motifs alone insufficient for K562.
- eval_10 mean=+0.0065 (K562=+0.0124) was strong though.

## Implication
- K562-specific motifs are LOAD-BEARING for K562 r. Don't drop them.
- Universal motifs help eval_10 but not eval_01.

## Next (exp 021)
Hybrid bimodal:
- 12.5k K562-saturated synthetic (exp 012 design) + 12.5k matched null GC25
- 12.5k HepG2 real H3K27ac peaks + 12.5k dinuc-shuffled HepG2 nulls
Goal: K562 lift from synthetic, HepG2 lift from real peaks. Each sub-bank
has its own paired null so both predictors see clean 50/50 splits.
