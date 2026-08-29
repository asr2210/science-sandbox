# Exp 012 — chr18 (AT-rich, 40% GC) tiles

50k 200bp windows from human chr18.

## Result

| metric  | chr22 (47% GC) | chr18 (40% GC) |
|---------|---------------:|---------------:|
| eval_01 | 0.3202         | 0.3043         |
| k562    | 0.1443         | 0.1438         |
| hepg2   | 0.1990         | 0.1978         |
| sknsh   | 0.6173         | 0.5715         |

HepG2 SATURATED at ~+0.20 — going more AT-rich didn't push it further.
SKNSH dropped 0.046 because chr18 GC drifts below SKNSH's 50%-GC peak.
Net: chr18 is WORSE.

Lesson: HepG2 score has a ceiling around 0.20 just from genomic-natural
sequences. To go higher need either cell-type-specific functional
sequences (DHS peaks) or specific motif enrichment that doesn't disturb
SKNSH.
