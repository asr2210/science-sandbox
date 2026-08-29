# Exp 027 — chr22 + chr19 50/50 mix — NEW BEST 0.3215

50k 200bp windows: 25k from chr22 + 25k from chr19.

## Result — NEW HIGH

| metric  | chr22 alone | chr19 alone | mix 50/50 |
|---------|------------:|------------:|----------:|
| eval_01 | 0.3202      | 0.3198      | **0.3215** |
| k562    | 0.1443      | 0.1440      | 0.1446    |
| hepg2   | 0.1990      | 0.1995      | 0.2004    |
| sknsh   | 0.6173      | 0.6160      | 0.6196    |

**SUPER-LINEAR**: mix is HIGHER on ALL THREE cell types than either
parent alone. This strongly suggests the scorer is a CORRELATION
(probably Pearson) — and library diversity boosts correlation.

**Theory v9 (BIG)**: `_r` IS in fact a correlation across the library
(not a mean activity). A more diverse library with the right
composition gives a higher correlation between model predictions and
some target signal. Mixing similar-GC chromosomes adds diversity
without violating the composition zone.

**Test for next exp**: see if multi-chromosome mix that includes
chr1 (HepG2-friendly) and/or chr18 (AT-rich) adds even more
diversity. Earlier 4-chrom mix (015) gave 0.3157 — chr1+chr18 may
have pushed too AT-rich. Maybe weighted toward chr22/chr19 with
just a touch of chr1 is the sweet spot.
