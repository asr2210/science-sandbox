# 007 — Top DNase peaks duplicated 10x

5000 top-signal DNase peaks (any of K562/HepG2/SK-N-SH), each duplicated 10x → 50,000 lines / 5,000 unique.

**Result:** mean_r ~ -0.001 broadly. eval_08 HepG2 = 0.0129 (highest seen for that cell type so far). eval_10 K562 = 0.0102.

**Interpretation:** Duplication didn't help mean. Top-DNase peaks may also be too peaked in K562. The model probably overfits the 5k unique sequences and predicts noise for everything else.
