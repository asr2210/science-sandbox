# Eval Set Structure (discovered from exp 001)

prepare.py reports 14 eval sets but several are **duplicates** (identical
mean_r/k562_r/hepg2_r/sknsh_r values on random uniform input). Confirmed
pairs from exp 001:

| Equivalent sets | mean_r on random uniform |
|---|---|
| eval_01 ≡ eval_14 | 0.0619 |
| eval_02 ≡ eval_05 | 0.0601 |
| eval_03 ≡ eval_12 | 0.0756 |
| eval_04 ≡ eval_09 | 0.0737 |
| eval_06 ≡ eval_11 | 0.0615 |

Distinct sets (9):
- eval_01 (=14) — **primary metric**
- eval_02 (=05)
- eval_03 (=12)
- eval_04 (=09)
- eval_06 (=11)
- eval_07
- eval_08
- eval_10
- eval_13

## How to use this
- When optimizing, focus on the **9 distinct sets**, especially eval_01.
- A reported gain on eval_07 alone is real; a gain on eval_01 also
  appears as a gain on eval_14 — don't double-count.
- Look at per-cell-type r when analyzing: a set whose per-cell scores
  differ widely on different libraries may be measuring a different
  property than one whose scores stay similar.
- Confirm the duplicates persist across runs (could be a coincidence
  if scores happen to round to the same 4 decimals, but the alignment
  on all four metrics — mean, k562, hepg2, sknsh — at exp 001 makes it
  very likely structural, not noise).

## Random-uniform baseline (exp 001)
For reference, "doing nothing" gets these scores:
- eval_01: 0.062, eval_02: 0.060, eval_03: 0.076, eval_04: 0.074,
  eval_06: 0.062, eval_07: 0.122, eval_08: 0.044, eval_10: 0.118,
  eval_13: 0.122.
Any new library should beat these. The "easy" sets (07, 10, 13) likely
have simpler structure; eval_08 is hardest.
