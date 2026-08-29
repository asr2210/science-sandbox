# Experiment 004 — DHS quintile-stratified library

## Design
50K windows from human DHS Index, 10K from each of 5 mean_signal
quintiles. Random offset within window. No mouse, no random genomic.

## Result
- eval_01: 0.392 (Δ -0.002 vs exp 002)
- K562: 0.602, HepG2: 0.426, SK-N-SH: 0.148

## Interpretation
Pure DHS coverage stratified by signal — slightly worse than the
4-way mix. The activity-range stratification is good but I gave up
the random genomic content that exp 002 had. Cannot disentangle
"activity stratification helps" from "loss of random-genomic hurts"
in this design.

## Implication
Need a cleaner test of activity range: keep the random-genomic baseline,
ADD active-vs-inactive contrast on top.
