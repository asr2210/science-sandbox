# Exp 016 — cCRE dELS (distal enhancer-like) only

50k 200bp windows centered (±50bp jitter) on ENCODE V4 dELS elements
from chr1/18/19/22.

## Result

| metric  | chr22 random | dELS only | mixed cCRE (010) |
|---------|-------------:|----------:|-----------------:|
| eval_01 | 0.3202       | 0.3118    | 0.3077           |
| k562    | 0.1443       | 0.1425    | 0.13             |
| hepg2   | 0.1990       | 0.1865    | 0.18             |
| sknsh   | 0.6173       | 0.6063    | 0.61             |

dELS slightly better than mixed cCRE (no high-GC PLS pollution) but
still below pure chr22 random. The slight GC-shift up (48.1% vs ~47%)
trims HepG2.

Lesson: even the "cleanest" enhancer class is enriched for GC content
that hurts our HepG2 score. Random genomic tiles remain the strongest
single recipe.

Pivot: stop selecting BY ANNOTATION. Try selecting BY COMPOSITION —
chr22 tiles filtered to drop very GC-rich windows (CpG islands) but
keep the broader spread (30-55%).
