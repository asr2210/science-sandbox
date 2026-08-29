# 005 — mixed density library

**Hypothesis**: variance hypothesis — mixing densities will boost score above uniform 6/seq.

**Design**: 10k seqs each at densities 0, 3, 6, 9, 12 using the safe 10-motif panel.

**Result**: eval_01 = **0.2345**. WORSE than uniform 6 (002 = 0.268).

**Big insight**: `mean_r == (k562_r + hepg2_r + sknsh_r) / 3`. Verified on exp 001: (0.136-0.074+0.630)/3 = 0.231 = mean_r. So `mean_r` is literally the average of the three cell-line correlations.

**Interpretation**: mean_r of 005 ≈ weighted average of per-subset r values across densities. Mixing densities approximately averages individual subset performances. Since 6-motif is best, mixing pulls average down. NOT a variance-correlation effect.

Implication: the score is **per-sequence average**, not whole-library variance. To maximize, every sequence should be designed individually for max activity.

**Next**: focus on per-cell-line improvement. HepG2 has biggest gap (0.04 → maybe 0.15). K562 stuck at 0.13 — try K562-specific designs. Don't lose SKNSH 0.63 ceiling.
