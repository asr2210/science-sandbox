# Experiment 029 — exact 013 with SEED=1 (variance test)

## Design
IDENTICAL to 013 except SEED=1 instead of SEED=0.
- 15K uniform + 5K CTCF + 5K DNH3 + 25K paired 1500-3000bp flanks

## Result — mean_r 0.150 (vs 013's 0.166)
**Drop of 0.016 from seed change alone.**
- eval_06/11 = 0.195 (013=0.218, lost 0.023)
- eval_10 = 0.133 (013=0.151, lost 0.018)
- eval_07 = 0.152 (013=0.177, lost 0.025)
- eval_13 = 0.150 (013=0.126, GAINED 0.024)
- eval_08 = 0.035 (013=0.036, similar)

## Interpretation — CRITICAL FINDING
**Single-experiment scores have ~±0.01-0.015 stochastic noise from
RNG seed choice alone.** Many of our "underperforming" experiments
(014: 0.159, 015: 0.161, 020: 0.156) may not be meaningfully
different from 013's 0.166 — they could all be within noise.

This rewrites our interpretation:
- 013's 0.166 may be a **+0.008 lucky deviation** from a true mean
  of ~0.158 for the 013 design family.
- Most experiments differ by <0.01 from this true mean and are
  effectively noise.
- Only catastrophic-failure experiments (017, 023, 026 at 0.14-0.15)
  reflect REAL signal loss.

The TRULY best designs are likely those with mean across seeds
≥ 0.16. We've identified the WINNING DESIGN PATTERN (013 family),
just not a single best execution.

## Next
030 = **multi-seed 013**. Use TWO seeds to sample the 25K positives
and 25K flanks, hoping that averaging reduces variance and gives
a more robust score.
