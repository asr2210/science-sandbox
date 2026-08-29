# 010 random uniform GC=0.70

50k 200bp sequences, fixed GC=0.70. Seed 0.

## Result
- mean_r = 0.835 (eval_01 = 0.850)
- Below GC=0.6 (0.857) — peak is at 0.6
- SKNSH saturated at 0.95 (best across all experiments)
- HepG2 collapsed to 0.80 (was 0.86-0.88 at GC=0.5-0.6)
- K562 dropped to 0.78

## Takeaway
Going higher GC trades SKNSH gains for bigger HepG2 losses. Peak is around
GC=0.6. Curve is concave.

## Skill update
Capture as `skills/gc_cell_preference.md`: SKNSH strongly prefers GC-rich,
K562 prefers GC-balanced, HepG2 prefers GC=0.5. Net optimum GC=0.60.
