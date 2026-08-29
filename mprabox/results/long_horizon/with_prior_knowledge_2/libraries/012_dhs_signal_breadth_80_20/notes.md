# 012_dhs_signal_breadth_80_20

## What I tested
Push the 70/30 winner (011) further: 80% mean_signal-weighted (40K) +
20% numsamples-weighted (10K). Brackets the optimum signal-share.

## Result — collapse
| metric   | 012    | 011 (70/30) | 003 (50/50) | Δ vs 011 |
|----------|--------|-------------|-------------|----------|
| eval_01  | 0.7055 | 0.7383      | 0.7327      | -0.033   |
| eval_07  | 0.7309 | 0.7751      | 0.7618      | -0.044   |
| eval_08  | 0.6523 | 0.7041      | 0.6984      | -0.052   |
| eval_13  | 0.7229 | 0.7644      | 0.7469      | -0.042   |
| cross-14 | 0.7433 | 0.7811      | 0.7735      | -0.038   |

Per-seed eval_01: 0.6892 / 0.6913 / 0.7360 (std ≈ 0.022 — wide).

The trajectory 50/50 → 70/30 → 80/20 = 0.7735 → 0.7811 → 0.7433.
Asymmetric peak around 70/30, sharp dropoff toward 80/20.

## Why it collapsed
Two compounding causes:
1. **Below the breadth-stability floor.** 10K elements drawn from a
   numsamples-weighted distribution gives a noisy, unstable subsample
   of the breadth axis (per-seed std jumped from 0.002 in 011 to 0.022).
2. **Loss of breadth signal** below the threshold needed for the
   cell-type-invariant grammar to register — eval_08 (the diversity-
   sensitive eval) lost the most (-0.052).

There is a critical mass per axis below which the axis effectively
disappears from the library. For numsamples, it appears to be around
12-15K (003's 25K and 011's 15K both work; 012's 10K does not).

## Theory update
The "asymmetric mix proportional to standalone strength" heuristic from
011 has a floor: each axis must clear a minimum sample-count threshold
to provide stable signal. Beyond that, the relative weight follows
standalone strength. This is a NON-MONOTONE optimum — pushing the
strongest axis even higher passes a stability cliff.

## Next
Bracket the peak with 60/40 to confirm 70/30 is local optimum, then
pivot to test orthogonal levers from the new 70/30 baseline.
