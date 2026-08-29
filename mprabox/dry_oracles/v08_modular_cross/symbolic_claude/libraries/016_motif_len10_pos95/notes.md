# 016 — motif length 10 at pos 95, 4 buckets

- mean_r eval_01: 0.0025 (down from 0.0061 in exp 5).
- BUT eval_08: 0.0099 (condition_a 0.0201 — highest single value yet!)
- eval_10: 0.0048 (best for that eval).
- Confirmed length 20 sweet spot for eval_01.
- Different evals prefer different motif lengths AND positions.

## Per-eval best across all experiments so far
| eval | best mean_r | source |
|------|-------------|--------|
| 01   | 0.0061 | 005 |
| 02   | 0.0060 | 005 |
| 03   | 0.0074 | 005 |
| 04   | 0.0042 | 014 |
| 05   | 0.0060 | 005 |
| 06   | 0.0072 | 005 |
| 07   | 0.0030 | 004 |
| 08   | 0.0099 | 016 |
| 09   | 0.0042 | 014 |
| 10   | 0.0052 | 006 |
| 11   | 0.0072 | 005 |
| 12   | 0.0074 | 005 |
| 13   | 0.0097 | 010 |
| 14   | 0.0061 | 005 |

005 wins 7 of 14 evals (the duplicates: 01,14 and 02,05 and 06,11 and 03,12).
So really 005 wins 4 unique evals out of 9 distinct. Position 0 / shorter
motif wins for evals 08, 13.
