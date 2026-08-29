# Exp 019 — period-3 (0,1,2) at p=0.7

## Result
eval_01 mean_r = 0.0957. condition_c = 0.2495 (vs ~0.41 for period-4).
Much worse than period-4.

## Interpretation
Period-4 isn't generic "any cycle works". The scorer specifically
rewards period-4. Score halves when we use period-3.

## Next
Try per-sequence random phase shift of period-4: each sequence picks
phase ∈ {0,1,2,3} independently, then uses (phase + i) mod 4 as its
template. Library has all phases at each position (might lift a/b),
but each row still has strong period-4 (preserves c).
