# 009 4mer_scan_random_bg

50,000 random uniform sequences + cycle through all 256 4-mers inserted at center.

## Result
eval_01 = -0.0017 (within noise of baseline 0.0013).
eval_10 = +0.0027 (small positive). Mostly negative across evals.

## Interpretation
Single 4-mer at center has marginal effect — motif content is only 4/200 = 2% of sequence,
dominated by background random. Signal too weak.

For eval_01: condition_b dropped (-0.0003 vs random 0.0067), so the motif insertion
disrupted condition_b's preference for pure randomness, without helping enough on a or c.

## Best for eval_01 so far
| Exp | mean_r | notes |
|---|---|---|
| 005 dirichlet(0.5) | +0.0030 | best |
| 001 random | +0.0013 | baseline |
| All others | ≤ 0.0013 or negative |

Going to try shotgun library next (maximum within-set diversity).
