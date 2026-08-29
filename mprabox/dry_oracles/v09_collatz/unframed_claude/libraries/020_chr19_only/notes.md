# Exp 020 — chr19 only (48% GC)

50k 200bp windows from chr19, which has slightly higher GC than chr22.
GC mean=0.481.

## Result

| metric  | chr22 (009) | chr19 (020) |
|---------|------------:|------------:|
| eval_01 | 0.3202      | 0.3198      |
| k562    | 0.1443      | 0.1440      |
| hepg2   | 0.1990      | 0.1995      |
| sknsh   | 0.6173      | 0.6160      |

Effectively TIED with chr22. The scorer is indifferent to chr19 vs
chr22 (both at ~47-48% GC, same composition). Confirms the "natural
DNA ceiling" hypothesis: any natural DNA in this GC zone gives ~0.32.

This is now our 4th confirmation that 0.32 is a hard ceiling for
random natural DNA tiles. The K562/HepG2/SKNSH per-cell-type scores
all cluster within 0.005 of their chr22 values across many recipes.

**Strategic implication**: pure natural-tile recipes likely cannot
break 0.322. To push further need either (a) hand-crafted sequences
that the models score uncommonly high, or (b) accept that 0.32 is
the asymptote and stop trying to filter.
