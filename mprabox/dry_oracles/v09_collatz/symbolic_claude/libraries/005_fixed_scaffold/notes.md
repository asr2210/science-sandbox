# 005 — Fixed scaffold prefix (48 chars) + uniform tail

Prefix "01230123...01230123" length 48 (12 repeats), shared across
all 50k sequences. Suffix length 152 uniform random.

## Result
- eval_01: mean_r=0.2661 (vs 0.2399) — UP by 0.026
- a: 0.137 (unchanged), b: +0.01 (was -0.05!), c: 0.65 (slightly up)
- eval_07 jumped to 0.28, eval_13 to 0.27, both above their previous
  values on baseline. eval_08 essentially unchanged.

## Interpretation
HUGE result. Cross-sequence alignment (same chars at same positions)
boosts condition b without harming a or c. The diversity in the tail
preserves a; the structured prefix doesn't hurt c (maybe even helps).

This contradicts the simple "diversity vs structure trade-off"
picture from 003. Fixed-position scaffold delivers structure WITHOUT
collapsing diversity. Random-position motif (004) didn't because
there's no alignment.

Lever found. Next: push scaffold length to find the optimum.
