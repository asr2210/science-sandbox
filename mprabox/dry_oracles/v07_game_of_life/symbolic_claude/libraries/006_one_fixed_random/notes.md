# 006 — 50k copies of one fixed random sequence

The sequence uses all 4 chars. But all 50k copies are identical → at each position,
all sequences have the SAME char → variance across population is 0 at every position.

## Result
NaN on all evals.

## Decisive interpretation
**Scoring is population-level, not per-sequence.**

Specifically: at each position p and channel c (one of 4 chars), compute population
statistic. If population variance is 0 for any channel at any position → NaN.

This rules out per-sequence Pearson correlation interpretations.

## Updated model
At each position p, the empirical population distribution over the 50k sequences
is the input. The score involves correlating this distribution (or its per-channel
indicators) with a target.

## Implications for next experiments
- Every position must have all 4 chars represented across the population (non-zero variance).
- Per-channel population variance at every position is required.
- Population mean per position is one factor; higher moments may also matter.

## Puzzle
- Random uniform (exp 001): score 0.39
- 4 biased blocks averaged to uniform pop mean (exp 003): score 0.33 (different!)
- Population mean per position is SAME in both, yet scores differ. So the score
  depends on more than just population mean per position.
- Maybe it depends on how the 1s are distributed across the 50k vector (ordering or
  higher moments).

## Skill to extract
Add to skills/: "NaN avoidance: every position must have non-zero pop variance per channel"
