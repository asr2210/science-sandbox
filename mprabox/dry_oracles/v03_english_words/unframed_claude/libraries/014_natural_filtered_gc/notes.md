# Exp 014: natural windows filtered to GC in [0.45, 0.55]

**Hypothesis**: Removing wide per-seq GC variance from natural should
restore K562/HepG2 toward random while preserving natural motifs that
help SKNSH.

**Results**: eval_01=0.3987 (vs natural 0.3975, random 0.4235).
- K562: 0.536 (basically same as natural 0.541)
- HepG2: 0.551 (basically same as natural 0.552)
- SKNSH: **0.1094** ← best SKNSH yet, beats natural (0.099)

**Interpretation**: GC-filtering did NOT recover K562/HepG2 from the
natural penalty. So natural sequences have other features (beyond per-seq
GC variance) that drag K562/HepG2 down — likely repeat content, CpG
depletion, or specific dinucleotide patterns that random doesn't have.

But SKNSH improved further (+0.01 over unfiltered natural). The mid-GC
natural sequences are the most informative for SKNSH.

**Implications**: 
- K562/HepG2 want random — period. Anything from natural sources hurts them.
- SKNSH wants natural — and slightly more if GC is moderated.
- Trade-off remains fundamental.

Next: test if specific cCRE *subtypes* (promoter-like vs enhancer-like)
behave differently — maybe promoters score higher than enhancers.
