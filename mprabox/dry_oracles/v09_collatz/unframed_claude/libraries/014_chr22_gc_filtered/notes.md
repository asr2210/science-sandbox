# Exp 014 — chr22 windows filtered to 45-50% GC

50k chr22 200bp windows where local GC is 45-50% (the "sweet band").

## Result — disastrous

| metric  | chr22 unfiltered | chr22 mid-GC |
|---------|-----------------:|-------------:|
| eval_01 | 0.3202           | 0.0438       |
| k562    | 0.1443           | -0.1308      |
| hepg2   | 0.1990           | 0.0478       |
| sknsh   | 0.6173           | 0.2142       |

ALL three cell types crashed. SKNSH from 0.62 → 0.21.

Interpretation: filtering to mid-GC removed BOTH the GC-rich tail (CpG
islands, promoter-like sequences) and AT-rich tail (intergenic /
repeat-rich), keeping only a narrow band of mostly intronic / gene-body
sequence — a specific composition the model doesn't reward.

This also suggests SKNSH (and the others) reward LIBRARY GC DIVERSITY:
having sequences across the full GC spectrum is critical. Random uniform
50% has tight per-sequence GC but VERY UNIFORM bases (high entropy);
chr22 unfiltered has wide GC spread WITH natural composition.

**Strategy update**: preserve real-DNA character AND GC diversity.
