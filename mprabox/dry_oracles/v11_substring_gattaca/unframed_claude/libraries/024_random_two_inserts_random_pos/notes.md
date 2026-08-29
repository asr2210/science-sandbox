# 024 — 25k strict + 25k random with 2 8-mer inserts at RANDOM positions

## Hypothesis
Random-position 2-inserts (vs 020's fixed positions) may avoid the
position-rigidity penalty.

## Result
- eval_01 mean=**0.8779** (K562 0.8541, HepG2 0.9056, SKNSH 0.8740)
- vs 020 (2 fixed): +0.0005
- vs 017 (1 insert): -0.004

## Interpretation
Random positions slightly better than fixed for 2-insert (matches 017
where 1 insert is at random pos), BUT 2 inserts still worse than 1.
SKNSH did get a slight boost (+0.002), but K562 dropped (-0.008).

## Lesson
1 insert per random sequence is the cluster-strength sweet spot.

## Next
025: try mixing recipes — 014's 3-motif + 017's 50-bank.
