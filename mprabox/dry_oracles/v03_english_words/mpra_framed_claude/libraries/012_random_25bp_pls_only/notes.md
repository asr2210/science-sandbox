# 012 — Random + 1x25bp PLS-only fragment per sequence

**Design.** As 008 (25bp insert in random) but fragments drawn ONLY from PLS (promoter-like, n=47K available, sampled to 50K with replacement).

**Result.** eval_01 = **0.4248** — **FIRST library to BEAT random (0.4192)**. K562 = 0.591 (≥ random), HepG2 = 0.619 (≈ random), SK-N-SH = 0.065 (+44% over random's 0.045).

| | K562 | HepG2 | SK-N-SH | eval_01 |
|---|---|---|---|---|
| 001 random | 0.590 | 0.623 | 0.045 | 0.4192 |
| 008 mixed 25bp | 0.582 | 0.610 | 0.060 | 0.4174 |
| **012 PLS 25bp** | **0.591** | **0.619** | **0.065** | **0.4248** |

**Interpretation — PLS is the highest-info biology subset.** Promoter-like elements:
- Have strong MPRA activity (higher signal-to-noise per bp).
- Contain canonical promoter motifs (Inr, TATA, NFY, SP1 — broadly active across cell types).
- Are universally cross-cell-active (vs. cell-type-specific enhancers).

Embedding 25bp PLS fragments in random:
- Preserves random's compositional advantage (K562/HepG2 r unchanged or slightly improved).
- Adds biology that lifts SK-N-SH by 44%.

**Theory v10.** The ideal biology to embed in a random background is the SHORTEST, HIGHEST-ACTIVITY biology available. PLS provides strong activity drivers (core promoter motifs) per bp than dELS (distal enhancers with more diverse, less universally-active grammars).

**For generalization to UNSEEN cell types**: core promoter motifs (TATA, Inr, SP1, NFY) are universally active in most cell types. A library trained with PLS embedding should generalize better to ANY cell type whose promoters use these elements — which is essentially all of them.

**Next.** Combine the two wins: 3x10bp distributed PLS-only fragments (best of 011's distribution + 012's PLS source).
