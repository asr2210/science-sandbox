# 001 probe strata

## Design
6 strata of ~8333 contiguous sequences:
- A: uniform random
- B: all '0' constant
- C: GC-rich (1,2 favored)
- D: AT-rich (0,3 favored)
- E: '0123' periodic
- F: random with motif '12102' inserted every 20bp

## Result
eval_01 mean_r = 0.5436 (k562=0.4985, hepg2=0.6301, sknsh=0.5022)
mean across 14 evals ~ 0.51
eval_08 outlier low (0.13); eval_07 best (0.60); eval_13 (0.57); eval_10 (0.55)

## Key findings
1. result.json gives ONE score per eval, no per-row breakdown. Cannot do
   in-library stratum analysis from one submission.
2. Eval duplicates: eval_01==eval_14, eval_02==eval_05, eval_03==eval_12,
   eval_04==eval_09, eval_06==eval_11. So ~9 unique evals out of 14.
3. eval_08 is unusually low (0.13). Either it's a different metric or our
   strata happened to be antagonistic to it.
4. Scoring is fast (~31s, n_seeds=1) so submissions are cheap to evaluate.
5. Despite 1/6 of seqs being all-constant '0' and 1/6 being '0123' repeat,
   we still get r~0.54. So the metric must produce reasonable output even
   for degenerate inputs.

## Implications for theory
- The 14 evals are probably correlation-based ("_r" suffix, per-cell-line
  breakdowns). Likely: hidden ground-truth labels per row × cell line, and
  some hidden predictor maps our sequence at row i to a prediction. Pearson r
  computed across the 50k rows per cell line.
- Constant sequences would all get the SAME prediction, which in a Pearson r
  contributes 0 (no variance). So 1/6 constant strata effectively just
  removes 1/6 of the signal — explains why we still get reasonable r.
