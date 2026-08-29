# Experiment 021 — chr19 with per-seq mutation gradient (0-50%)

## Hypothesis
Wide across-library variance in "naturalness" should help r since
both scoring axes might track distance from natural DNA.

## Results
- eval_01: 0.0480 (chr19 baseline 0.0502) → same ceiling
- eval_08: 0.0798 (chr19 0.0551) → JUMPED (eval_08 loves variance)
- eval_10: 0.0348 (chr19 0.0299) → up

## Interpretation
The mutation gradient helps evals that respond to randomness
(eval_08, eval_10) but eval_01 doesn't budge. eval_01 has a real
ceiling ~0.05 with current approaches.

Useful side-finding: eval_08 strongly rewards across-library
RANDOMNESS variance — best on it might come from mut-gradient,
but not helpful for eval_01.

## Next
EXP 22: try chr19 windows ENRICHED for ENCODE TFBS clusters
(download from UCSC). These should be active regulatory regions.
