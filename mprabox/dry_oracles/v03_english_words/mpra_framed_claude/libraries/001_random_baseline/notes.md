# 001 — Random baseline

**Design.** 50,000 uniform i.i.d. random 200bp sequences (seed 0).

**Result.** mean_r ≈ 0.42 across most eval sets (eval_01 = 0.4192). Per-cell: K562 ≈ 0.59, HepG2 ≈ 0.62, SK-N-SH ≈ 0.045.

**Interpretation.**
- The model learns *substantial* K562/HepG2 signal even from uniformly random DNA. Compositional features (GC content, k-mer frequencies) and the rare random occurrence of short motifs apparently provide enough signal that K562/HepG2 r ≈ 0.6.
- SK-N-SH r is near zero (0.04). Two hypotheses:
  (a) SK-N-SH-driving motifs (neural TFs: NEUROD, REST, ASCL, OLIG, POU3F, PAX) are short, rare-in-random, and not learnable here.
  (b) SK-N-SH activity in random sequences has very low variance, so r is noisy — the model has no signal to fit.
- Eval sets cluster tightly (most mean_r = 0.418-0.428). eval_08 is an outlier (0.385) — interesting; likely a distinct distribution.

**For theory.** Random sequences are surprisingly informative — but the failure mode is asymmetric: K562/HepG2 ≫ SK-N-SH. A library tuned only on K562/HepG2-like compositional signal would not generalize to neural-like cells.

**Next.** Test whether genomic regulatory elements (real CREs) lift SK-N-SH and/or further raise K562/HepG2.
