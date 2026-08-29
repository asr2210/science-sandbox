# Experiment 010 — FANTOM5 enhancers (chr19+chr22)

## Hypothesis
Real regulatory regions (FANTOM5 active enhancers) should be in
the oracle's training distribution → higher r than genome-random.

## Method
3155 FANTOM5 enhancers on chr19+chr22. Pad short enhancers (<200bp)
with flanking, then sample 200bp windows weighted by length.

## Results
- eval_01: 0.0324 (chr19 random: 0.0502)  → WORSE
- avg: ~0.031

## Interpretation
Regulatory enrichment HURT. Together with CpG islands (also hurt),
this means the chr19/22 advantage is NOT from regulatory content.

Pattern emerging: regulatory regions are biased toward higher GC,
which we know hurts. The chr19 advantage over uniform random must
come from chr19's NORMAL-GC sequences, not its CpG-rich pockets.

## Theory update — T5
The lever is NOT regulatory content. The lever is "natural DNA at
canonical composition (~50% GC)". chr19/22 wins because most of
their windows happen to be near 50% GC. CpG islands and enhancers
shift the GC distribution away from optimum.

## Next
EXP 11: chr19 windows FILTERED to 40-50% GC. If this beats plain
chr19, GC filtering is a real lever.
