# 021 — 48% GC random background + 1x25bp PLS

**Design.** Like 012 but background sampled at 48% GC (A,T,C,G weights 0.26, 0.24, 0.24, 0.26) to compensate for CpG-rich PLS fragments. Target net composition ~49.5% GC.

**Result.** eval_01 = **0.4157** vs 012's 0.4248 (Δ-0.0091). K562 = 0.582, HepG2 = 0.608, SK-N-SH = 0.057.

| | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 001 random (50% GC) | 0.590 | 0.623 | 0.045 | 0.4192 |
| 012 50% GC + PLS | 0.591 | 0.619 | 0.065 | **0.4248** |
| 021 48% GC + PLS | 0.582 | 0.608 | 0.057 | 0.4157 |

**Interpretation — eval composition is exactly 50% GC.** The 2% downshift in background composition hurt BOTH K562 and HepG2 (by ~0.009 and ~0.011), confirming that uniform 50% GC IS optimal for the eval distribution. SK-N-SH also dropped slightly (likely because the 2% lower GC fragments give weaker motif-context signal — many promoter motifs are GC-rich).

**Theory v19 — eval composition is uniform 50% GC.** Random sampled at exactly 25% per base is the composition target. Any composition shift hurts at least one of K562/HepG2 noticeably. The HepG2 -0.004 in 012 vs random is real composition cost, but cannot be recovered by background compensation — that just moves the loss elsewhere.

**Next.** 022 — try smaller PLS payload (1x15bp PLS). 009 (1x15bp mixed cCRE) lost to 008 (1x25bp mixed), but PLS-specific 15bp may behave differently — if 15bp captures core motif well and disturbs composition less, it could beat 012.
