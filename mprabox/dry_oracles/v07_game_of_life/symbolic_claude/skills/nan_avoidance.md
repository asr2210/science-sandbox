# NaN avoidance

The scoring function returns NaN if ANY position lacks non-zero population variance
for any of the 4 channels (chars 0,1,2,3).

## Rules to prevent NaN
1. Each character {0,1,2,3} must be present at every position somewhere in the population.
2. Equivalently: for each position p and char c, at least 1 sequence (and at most 49,999)
   must have char c at position p.

## Known NaN-producing libraries
- Single fixed string × 50k copies: each position has the same char (var=0).
- Constant string (e.g., all 0s): every position constant, every channel zero variance.
- Sub-alphabet (e.g., only chars 0,1): channels 2,3 are zero everywhere.

## Safe approaches
- Random sampling with non-zero prob for each char at each position.
- Mixed bias (every char gets at least some probability).
- Even with strong bias (70%/10%/10%/10%), each char appears → safe.
