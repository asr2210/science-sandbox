# 003 — dense broad motif panel

**Hypothesis**: more motifs + broader cell-type-specific panel will push score above 0.27.

**Design**: 50,000 × 200bp random backbone, 12 motifs per seq, 18-motif panel (added GATA1, KLF1, TAL1, RUNX1, PU.1, NFE2, CEBPA, FOXA1, ZIC, NRF1).

**Result**: eval_01 mean_r = **0.2129** (DOWN from 002's 0.2675 by 0.055).
- HepG2 went negative again (-0.0895). 
- SK-N-SH dropped (0.596 vs 0.627 in 002).
- K562 essentially unchanged.

**Interpretation**: density 12 + broader panel is HARMFUL. Two competing hypotheses:
  H1: density too high (saturates / destroys backbone context)
  H2: some new motifs are actively repressive (CEBPA TTGCGCAAT shares a motif with NRF1; TAL1 CAGGTG / E-box collisions with CAGCTG; ZIC CCATATGG contains TATA-like)

Need to disentangle in next experiment.

**Next**: Exp 004 = 002's panel at density 10 (test density alone, holding identity fixed).
