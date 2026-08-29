# Experiment 020 — chr19 repeat-only DIFFERENT SEED (noise check)

## Method
Same generate.py as exp 16, seed=2020 instead of 16.

## Results
- eval_01: 0.0488 (exp 16 chr19 repeat-only: 0.0518)
- Difference: ~0.003 across seeds (library-side variance)

## Interpretation
Library sampling variance is ±0.003 on eval_01. The 0.0518 from
exp 16 was lucky sample. True value ~0.050, basically same as
plain chr19 (0.0502).

**KEY INSIGHT**: The 0.052 "best" was within noise of all-chr19
results. There is no real lever among the natural-DNA variants
I've tested. Ceiling on eval_01 is ~0.050 ± 0.003.

## Next
Try a non-natural-DNA lever or accept ~0.050 as ceiling. Plan:
EXP 21 — ENCODE cCREs (active regulatory elements) downloaded
from UCSC if accessible.
