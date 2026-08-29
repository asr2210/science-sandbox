# 010_dhs_signal_breadth_ccremaxz_3axis

## What I tested
003 winning recipe + a third additive axis weighted by ENCODE cCRE
maxZ (max z-score of any cCRE overlapping the DHS, max across DNase
+ H3K27ac + H3K4me3 + CTCF). 16,667 from each of three axes.

The cCRE_maxZ axis only draws from cCRE-overlapping DHS (1.35M of
3.59M elements, 37.7% of pool).

## Result — slight loss
| metric   | 010    | 003    | Δ      |
|----------|--------|--------|--------|
| eval_01  | 0.7179 | 0.7327 | -0.015 |
| eval_07  | 0.7439 | 0.7618 | -0.018 |
| eval_08  | 0.6785 | 0.6984 | -0.020 |
| eval_09  | 0.8545 | 0.8685 | -0.014 |
| eval_13  | 0.7318 | 0.7469 | -0.015 |
| cross-14 | 0.7586 | 0.7735 | -0.015 |

Per-seed eval_01: 0.7308 / 0.7308 / 0.6920 (std ≈ 0.022).

## Why it didn't help
Same root cause as 008: cCRE-derived metrics (whether class label or
maxZ score) are computed from ENCODE multi-mark data that has heavy
overlap with the DHS Index's own DNase signal. mean_signal is itself
a DNase-derived metric, so cCRE_maxZ is largely correlated with
mean_signal — the third axis selects elements that are already
preferentially picked by the mean_signal axis.

The net effect: we lose 1/3 of our element-diversity budget to
re-select elements similar to those already selected by axis 1
(mean_signal). The pool drawn is more redundant, not more diverse.

## Implication
**ENCODE annotation derivatives (cCRE class, cCRE maxZ) do NOT add
orthogonal information to mean_signal + numsamples for this task.**
They are downstream of the same data.

To find a real third axis, the next experiment must use either:
- A different data type entirely (motif content from sequence, TF
  ChIP-seq from independent assays, cross-species conservation as
  a SUBSET).
- Or accept that the 003 mix is near the ceiling for DHS-derived
  axes, and pivot to a structural test (sample with replacement,
  different mixing ratio).
