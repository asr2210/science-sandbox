# 008 — 60% GC backbone + 002 motifs

**Hypothesis**: K562 is GC-driven. Higher GC backbone may push K562 above 0.13.

**Design**: backbone sampled with 30% G, 30% C, 20% A, 20% T (60% GC). Same 10-motif panel as 002, density 6.

**Result**: eval_01 = **0.1724** (DOWN). K562 = **-0.076** (massive crash from +0.13!). HepG2 = +0.041 (unchanged). SK-N-SH = 0.553 (lost).

**Key finding**: K562 IS GC-sensitive, but in the OPPOSITE direction. K562 model wants LOW GC. SK-N-SH also prefers lower GC. HepG2 is GC-insensitive.

Linear extrapolation from 50% GC (K562=0.136) → 60% GC (K562=-0.076):
  slope ≈ -2.12 per fraction GC
  predicted 40% GC: K562 ≈ +0.348
  predicted 30% GC: K562 ≈ +0.560

If extrapolation holds (even approximately), driving GC to 30-40% could push mean_r from 0.27 to 0.4+ via K562 alone, IF SK-N-SH and HepG2 don't collapse.

**Next**: Exp 009 = 40% GC + 002 motifs. Single-variable change. Check K562 and SK-N-SH responses.
