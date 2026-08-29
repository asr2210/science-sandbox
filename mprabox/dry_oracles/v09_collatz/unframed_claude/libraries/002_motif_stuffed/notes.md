# 002 — motif-stuffed library

**Hypothesis**: known activator motifs (AP-1, CRE, SP1, ETS, CCAAT, HNF, GATA, KLF, EBOX) increase predicted activity.

**Design**: 50,000 × 200bp uniform random backbone, then insert 6 randomly chosen motifs from panel of 10 at random non-overlapping positions.

**Result**: eval_01 mean_r = **0.2675** (+0.037 vs 001)
- Per-cell: K562=0.138 (≈0 change), HepG2=+0.038 (was -0.074, Δ=+0.112), SKNSH=0.627 (slight decline)

**Interpretation**:
- Motifs work — especially for HepG2 model.
- Big chunk of remaining gap = K562 (0.14) and HepG2 (still only 0.04).
- SK-N-SH is already at its baseline ceiling for random-looking sequences.

**Next**: try dense motif packing, then cell-type-specific libraries.
