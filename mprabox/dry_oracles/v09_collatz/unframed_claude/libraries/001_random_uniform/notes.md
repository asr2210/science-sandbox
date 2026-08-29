# 001 — Random uniform baseline

**Hypothesis**: uniform random sequences establish a null baseline.

**Design**: 50,000 × 200bp, each base i.i.d. uniform over {A,C,G,T}, seed 42.

**Result**: eval_01 mean_r = **0.2307**
- K562_r = 0.1361, HepG2_r = -0.0742, SK-N-SH_r = 0.6302
- 13 of 14 eval sets are very similar; eval_08 is an outlier (0.0864)
- SK-N-SH "loves" random sequences already; HepG2 actively dislikes them

**Updates to theory**:
- HepG2 negative score on random suggests random looks ANTI-correlated with HepG2 enhancer target. To improve mean_r meaningfully we likely must push HepG2 from negative toward positive.
- SK-N-SH near 0.63 already suggests the score may saturate; harder to improve.
- eval_08 is a different beast — possibly a stricter held-out test or different model.

**Next**: probe whether GC content / motif insertion changes the score.
