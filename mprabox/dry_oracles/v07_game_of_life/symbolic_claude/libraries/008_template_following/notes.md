# 008 — Template following (90% match)

50k sequences each 90% matching a fixed random base template (seed 23), 10% random other.

## Result
- eval_01: 0.1943 (drop of 0.20 from random)
- All evals dropped substantially.

## Cross-reference matrix
| exp | per-pos pop | per-seq comp | score eval_01 |
|-----|-------------|--------------|---------------|
| 001 random uniform | uniform | uniform | 0.3943 |
| 003 4 bias blocks  | uniform | biased   | 0.3296 |
| 007 perfect uniform pop | exact uniform | uniform | 0.3938 |
| 008 template       | biased  | uniform  | 0.1943 |

## Interpretation
**Per-position uniformity matters MOST** (compare 003 vs 008: 003 keeps per-pos uniform
and only drops to 0.33; 008 violates per-pos uniformity and drops to 0.19).

**Per-sequence uniformity also matters** (003 vs 001: 0.33 vs 0.39 = 0.06 drop just
from per-sequence imbalance).

Both being uniform (001/007) is the current ceiling at 0.39.

## Next probe
Test exp 009: each sequence has EXACT per-sequence balance (50 of each char).
Should be even more "uniform" per-sequence than random Poisson. If this beats 0.39,
exact per-seq balance is rewarded.
