# 011_dhs_signal_breadth_70_30

## What I tested
003 winning recipe with mixing ratio shifted from 50/50 to 70/30:
35K mean_signal-weighted + 15K numsamples-weighted. Tests whether
003's 50/50 ratio was a free parameter or near a robust optimum.

## Result — clear win
| metric   | 011    | 003    | Δ      |
|----------|--------|--------|--------|
| eval_01  | 0.7383 | 0.7327 | +0.006 |
| eval_07  | 0.7751 | 0.7618 | +0.013 |
| eval_08  | 0.7041 | 0.6984 | +0.006 |
| eval_09  | 0.8702 | 0.8685 | +0.002 |
| eval_10  | 0.8103 | 0.8019 | +0.008 |
| eval_12  | 0.7005 | 0.6929 | +0.008 |
| eval_13  | 0.7644 | 0.7469 | **+0.018** |
| cross-14 | 0.7811 | 0.7735 | +0.008 |

**Wins on 13 of 14 evals.** Per-seed eval_01: 0.7405 / 0.7357 / 0.7386
(std ≈ 0.002 — extraordinarily tight, well below the noise floor).

This is the new champion. eval_13 (+0.018) and eval_07 (+0.013) — the
two cell-type-specific evals where breadth was hurting — are the
biggest gains. Tilting toward signal recovers cell-type-specific
signal that 003's 50/50 was diluting.

## Why it won
The 002 result already showed signal > breadth as a single axis on
eval_01 (+0.009). The 003 50/50 mix probably over-allocated to
breadth-only elements that don't carry as much per-element regulatory
information. Reallocating that budget to signal-weighted elements
(which can be cell-type-specific OR broad — the high-signal pool spans
both) gives the model more useful training examples.

The breadth axis still adds value at 30% (otherwise we'd see 001
levels), but its marginal contribution beyond ~30% is negative — past
that point each new breadth-driven element displaces a more
informative signal-driven one.

## Theory update
Quality axes have ASYMMETRIC weights when combined. The optimum is
not a uniform mix of equally-weighted axes — it's a tilted mix where
each axis claims a fraction proportional to its standalone strength.
For DHS-derived axes:
  signal contribution ≈ 0.7
  numsamples contribution ≈ 0.3

This may generalize: when adding future axes, allocate sample budget
proportional to single-axis performance.

## Next
- Run 012 = 80/20 to bracket the optimum.
- If 80/20 also wins, try 85/15 or 90/10.
- If 80/20 loses, optimum is at ~70/30.
