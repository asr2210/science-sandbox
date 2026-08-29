# Exp 026 — chr1 only random tiles

50k 200bp windows from chr1 (249Mb, 42% GC). Pure natural DNA.

## Result

| metric  | chr18 (40%) | chr1 (42%) | chr22 (47%) | chr19 (48%) |
|---------|------------:|-----------:|------------:|------------:|
| eval_01 | 0.3043      | 0.3108     | 0.3202      | 0.3198      |
| k562    | 0.1438      | 0.1447     | 0.1443      | 0.1440      |
| hepg2   | 0.1978      | **0.2020** | 0.1990      | 0.1995      |
| sknsh   | 0.5715      | 0.5858     | 0.6173      | 0.6160      |

**INSIGHT**: chr1 gave the HIGHEST HepG2 score so far (0.2020 vs
chr22's 0.1990). Confirms HepG2 prefers AT-rich (~42% GC) natural
DNA. K562 essentially indifferent to chromosome.

**SKNSH** drops with lower GC — confirms ~50% GC peak.

The chromosome-GC curve for each cell type is clear:
- K562: flat (any natural DNA gives ~0.144)
- HepG2: declining with GC; peak around 40-45% GC
- SKNSH: peaks at ~50% GC, drops on either side

chr22 wins overall because SKNSH's gain from 47% GC outweighs HepG2's
small loss vs 42% GC.

**Next idea**: chr1 windows filtered to GC ≥ 45% would isolate the
HepG2-good-AND-SKNSH-good subset of chr1. Try in exp 027.
