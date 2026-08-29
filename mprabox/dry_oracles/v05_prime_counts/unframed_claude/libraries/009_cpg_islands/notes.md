# Experiment 009 — CpG islands

## Hypothesis
Sample 200bp windows from CpG islands (chr19+chr22). High regulatory
density → maybe higher r if oracle likes regulatory regions.

## Method
3229 CpG islands on chr19+chr22 (UCSC cpgIslandExt). Sample windows
weighted by island length.

## Results
- eval_01: 0.0264 (chr19 random: 0.0502) → WORSE
- avg: ~0.022

## Interpretation
CpG islands HURT, likely because they are GC-rich (60-75%) — and
we know high GC is bad.

## Next
EXP 10: FANTOM5 enhancers (more regulatory, less GC-extreme).
