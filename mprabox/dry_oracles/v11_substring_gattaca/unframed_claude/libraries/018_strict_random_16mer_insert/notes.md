# 018 — 25k strict + 25k (random + 1 16-mer from 50-bank)

## Result
- eval_01 mean=**0.8723** (K562 0.855, HepG2 0.899, SKNSH 0.863)
- vs 017 (8-mer same bank): mean -0.010. HepG2 dropped most.

## Interpretation
Longer inserts hurt — likely the 16-mer pattern is too dominant a chunk of
the 200 bp sequence, distorting the random background's natural distribution
(HepG2 brittleness reappears).

## Lesson
Insert length sweet spot: ~8 bp. Longer disrupts; shorter probably gives no
lift.

## Next
- 019: insert in BOTH halves (strict + random), 8-mer 50-bank.
- 020+: explore other axes.
