# 006_dhs_mix_multiplicative

## What I tested
Single weighted draw: weight = `mean_signal × log(1 + numsamples)`. No
sample mixing — every element gets a single combined quality score.

## Result — loss
| metric   | 006    | 003 (best) | Δ      |
|----------|--------|------------|--------|
| eval_01  | 0.7028 | 0.7327     | -0.030 |
| eval_07  | 0.7209 | 0.7618     | -0.041 |
| eval_08  | 0.6506 | 0.6984     | -0.048 |
| eval_13  | 0.7086 | 0.7469     | -0.038 |
| cross-14 | 0.7404 | 0.7735     | -0.033 |

Per-seed eval_01: 0.6838 / 0.6759 / 0.7488 (std ≈ 0.040 — wide).

## Why it lost
Multiplicative weighting collapses the sample to the **intersection** of
"high-signal" AND "high-breadth" elements — disproportionately Stromal A
(median ns=116) and Tissue invariant. The library becomes redundant:
many sequences from the same regulatory class.

The 003 additive scheme keeps two distinct pools — pure-signal elements
(includes high-signal cell-type-specific) and pure-breadth elements
(includes lower-signal but ubiquitous). The union spans more of the
regulatory space than the intersection.

## Major structural insight
**Quality axes must combine ADDITIVELY (sample mixing), not
multiplicatively.** Adding conservation as a third axis later (007+)
must use the same scheme: a third sample fraction with its own
weighting, not a third multiplicative term.

Cost: each new axis claims a fraction of the 50,000-budget. Combinatorial
blowup. Need to be selective about which axes earn a slot.
