# 011 — replicate 002 (seed 100)

**Hypothesis**: 002's 0.2675 is reproducible signal, not noise.

**Result**: eval_01 = **0.2347** (Δ = -0.033 from 002 of the SAME design).
- K562: 0.136 (002: 0.138) — reproducible (~0.001)
- HepG2: -0.055 (002: +0.038) — HUGE swing (~0.093), SIGN FLIPPED
- SK-N-SH: 0.623 (002: 0.627) — reproducible (~0.004)

**Critical finding**: HepG2_r has high variance across seeds of the SAME design (~±0.05). K562 and SK-N-SH are stable. So:
- All my "HepG2 went up/down by 0.05" findings could be largely noise.
- 002's +0.038 HepG2 was likely a LUCKY seed; true mean closer to 0.
- The "additions hurt HepG2" claim (003, 006, 010) may also be coincidence.

**Implication**:
- Real comparisons need HepG2 changes > 0.1 to be confident.
- True best-design mean_r is probably around 0.245 (avg of 002 & 011), not 0.267.
- To exceed noise, need designs that produce LARGE expected gains, not marginal motif swaps.

**Next**: try a fundamentally different design — clustered motifs (super-additive heterotypic interactions) — to see if a different DESIGN PARADIGM lifts above noise floor.
