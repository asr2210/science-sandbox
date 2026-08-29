# 003_period4_identical

## Setup
50,000 identical copies of "0123"*50.

## Results
All evals NaN — same as 002 (all zeros), despite intra-string variation.

## Key insight (diagnostic)
The correlation is NOT per-string-then-averaged. If it were, each of the 50K
identical strings would give the same defined r, and mean would be a number.
Instead → NaN means the score depends on **cross-row variance**.

Strong hypothesis: the score is computed by encoding our 50K×200 input as a
50K×200 (or 50K×800 one-hot) matrix and computing column-wise Pearson r vs a
fixed target. Identical rows → constant columns → undefined r everywhere.

This implies: **the row ordering matters** — row i in our submission lines up
with row i in some target. Our job is to pick the right value at each (row, col).
