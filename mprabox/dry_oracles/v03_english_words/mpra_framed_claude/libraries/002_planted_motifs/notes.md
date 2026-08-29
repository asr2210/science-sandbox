# 002 — Random background + planted canonical TF motifs

**Design.** 50,000 random 200bp sequences, each with 3-5 motifs from a panel of 61 canonical TF consensus sequences planted at random positions/strands. Panel spans K562, HepG2, SK-N-SH, and broadly-active TFs.

**Result.** eval_01 = **0.4121** (vs 0.4192 for random). Per cell: K562 ≈ 0.58 (Δ-0.01), HepG2 ≈ 0.61 (Δ-0.01), **SK-N-SH ≈ 0.044 (unchanged)**. All eval sets slightly worse than 001.

**Interpretation — surprising negative result.**
- Planting "biologically meaningful" motifs *did not help*. K562/HepG2 dropped marginally; SK-N-SH was identical (≈0).
- Most likely explanations:
  1. **Short consensus motifs are too weak**. Many of my motifs are 5-8bp consensus sequences (CACGTG, TGACTCA, GATAAG). These already occur frequently by chance in random 200bp, so planting more doesn't substantially change occurrence rate.
  2. **Activity in K562/HepG2 doesn't actually respond strongly to short single-motif planting**. Even canonical TFBSs need context (flanking sequence, cooperative binding, distance constraints).
  3. **Disrupting random composition hurt slightly**. The model was learning compositional features (GC, k-mer); replacing random bases with motif bases shifted composition without adding signal.
  4. **SK-N-SH genuinely isn't fitting**. Neither random nor planted motifs give the model a learnable signal. This suggests SK-N-SH activity needs genomic-context information not capturable by 200bp synthetic sequences.

**Theory update.** Motif planting in random backgrounds with short consensus sequences is *not* a viable lever. Either I need (a) real genomic regulatory sequences with their full grammar, (b) much longer/PWM-sampled motifs with intentional flanking, or (c) sequences designed by a model that already learned the grammar.

**Next.** Test genomic regulatory sequences (ENCODE cCREs) — the strongest "biology-aware" library. If they substantially beat random, biology context is the bottleneck; if not, the gap is small enough that we should focus on other levers.
