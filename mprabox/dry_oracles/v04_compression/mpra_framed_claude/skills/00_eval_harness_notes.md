# Eval harness behavior (empirical, from exp 001)

## Timing
- prepare.py wall time ≈ 60s for a 50k×200bp library (most spent on model
  training; the harness reports ~26s for its own "evaluating" phase).
- Budget: 30 experiments × ~1min = ~30min compute. Plenty of headroom.

## Output structure
- Writes `result.json` to the experiment directory.
- Returns scores for 14 eval sets, each with `mean_r`, `k562_r`, `hepg2_r`,
  `sknsh_r`.

## Empirically observed eval-set duplicates (from exp 001)
At 4-decimal precision the following eval sets returned **identical** values:
- eval_01 ≡ eval_14
- eval_02 ≡ eval_05
- eval_03 ≡ eval_12
- eval_04 ≡ eval_09
- eval_06 ≡ eval_11

So there are at most 9 distinct underlying eval sets across the 14 reports.
Treat correlated pairs as one signal.

## K562 vs HepG2
In exp 001 every eval set reported **identical k562_r and hepg2_r values to
4 decimals**. This is suspicious and may indicate the eval is reporting the
same model output for both cell types — or that random sequences happen to
produce the same correlation by coincidence. Watch this with a more
structured library before concluding.

## Random baseline scores (exp 001, seed 42)
mean across 14: 0.342. eval_01: 0.343. Easiest: eval_07 (0.450).
Hardest: eval_08 (0.110). eval_04/09 (0.304) also relatively hard.

## Rules
- Don't modify prepare.py; treat as black box.
- sequences_0.txt: exactly 50000 lines × 200 ACGT.
- Each experiment gets its own commit immediately.
