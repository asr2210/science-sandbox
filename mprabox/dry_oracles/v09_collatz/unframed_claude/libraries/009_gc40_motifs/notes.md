# 009 — 40% GC backbone + 002 motifs

**Hypothesis**: K562 will rise linearly with lower GC.

**Design**: backbone at 40% GC (20% A, 30% C, 30% G, 20% T → wait that's 60% AT... let me recheck. I used A=30%, C=20%, G=20%, T=30% = 40% GC). Same 002 motifs at density 6.

**Result**: eval_01 = **0.2195**. K562 = 0.136 (UNCHANGED from baseline). HepG2 = -0.080 (tanked back negative). SK-N-SH = 0.604 (slight loss).

**Big surprise**: K562 did NOT rise. It's stuck at ~0.135 across 40-50% GC. K562 has a CLIFF at 60% GC (crash to -0.08) but no slope toward lower GC.

Also HepG2 lost at 40% GC: HepG2 wants ~50% GC for motifs to work. Lower GC → motifs don't help HepG2.

Revised theory T10:
  - K562: plateau ~0.135 at 40-50% GC, cliff to ~-0.08 at 60%. Probably saturates at plateau; K562 is locked.
  - HepG2: motif-driven, ~50% GC optimal. 40% backbone disrupts motif effectiveness.
  - SK-N-SH: 50% GC random gives 0.63 ceiling.

So 50% GC is the sweet spot for all 3. Don't deviate.

**Next**: stop tuning GC. Refine motif composition at 50% GC.
