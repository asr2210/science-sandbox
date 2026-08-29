# 013 dirichlet_1p0

Pure Dirichlet(1.0) — uniform on 4-simplex.

## Result
eval_01 = +0.0001 (basically zero). **eval_08 = +0.0076** (new highest single-eval), eval_13 = +0.0034.

## Eval_01 alpha sweep summary
| alpha | a | b | c | mean |
|---|---|---|---|---|
| 0.1 | -0.0034 | +0.0022 | +0.0009 | -0.0001 |
| 0.5 | +0.0003 | +0.0070 | +0.0016 | **+0.0030** |
| 1.0 | +0.0035 | -0.0042 | +0.0008 | +0.0001 |
| inf | -0.0003 | +0.0067 | -0.0025 | +0.0013 |

Sweet spot at alpha=0.5. Beyond noise:
- alpha=0.5 condition_b is highest (+0.0070); alpha=1.0 b unexpectedly drops to -0.0042
- alpha=1.0 condition_a is highest (+0.0035)

Mean dominates at alpha=0.5 due to highest b.

## Next direction
Try BIASED mean Dirichlet — maybe AT-biased composition helps.
