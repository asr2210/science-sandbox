# 016 — Random + 1x25bp pELS-only fragment per sequence

**Design.** Same as 012 but fragments from pELS (proximal enhancer-like, 249K available) instead of PLS.

**Result.** eval_01 = **0.4201** vs 012's 0.4248 (Δ-0.0047) and vs random 0.4192 (Δ+0.0009).

| | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 001 random | 0.590 | 0.623 | 0.045 | 0.4192 |
| 016 pELS 25bp | 0.590 | 0.615 | 0.055 | 0.4201 |
| 012 PLS 25bp | 0.591 | 0.619 | 0.065 | **0.4248** |

**Interpretation — PLS specifically beats other promoter-related classes.** pELS:
- K562 = PLS (both 0.590) — same composition class.
- HepG2 slightly below PLS (0.615 vs 0.619) — slight composition cost.
- SK-N-SH = 0.055 (only +22%) vs PLS = 0.065 (+44%) — about HALF the SK-N-SH lift.

The SK-N-SH gap explains why PLS > pELS for cross-cell-type generalization. pELS sequences are classified as "enhancer-like" because they lack RNA-seq evidence of being TSS-proximal; their motif syntax is more variable and cell-type specific.

**Theory v14 — promoter-like > enhancer-like for universal generalization.** Even with the same spatial proximity to TSS, the regulatory grammar of PLS (RNA-seq-supported TSS) is more universal than pELS. The model's SK-N-SH gain comes from learning *universal* core promoter motifs that are active in all transcribed regions — PLS uniquely concentrates these.

**Next.** 017 — try CA-CTCF (CTCF-bound chromatin accessible regions). CTCF is the most universally bound architectural TF (active in all cell types). Test whether CTCF-anchored cCREs lift SK-N-SH similarly to PLS, or whether the promoter-specific motifs are what matter.
