# Experiment 010: Chromosome-balanced sampling

## Plan
Each of 24 chromosomes contributes ~2083 sequences. Tests whether
length-weighted vs equal-weighted matters.

## Result
- eval_01 mean_r = **0.1333** (K562=0.032, HepG2=0.172, SKNSH=0.196)
- WORSE than length-weighted (0.1387)
- K562 dropped most (0.049 → 0.032)

## Implication
Natural length-weighted distribution is closer to optimal. Over-sampling
small chromosomes (chr19, chr21, chr22, chrY) hurts. The "natural" sampling
distribution of human DNA matters.

## Status
exp 006 (length-weighted full-genome random) remains the best so far (0.1387).
The improvements from "more diversity" are saturating around there.

## Next
Probe whether 6-mer-Markov-generated sequences (matched local statistics) can
match exp 006. If yes, composition is dominant. If no, long-range structure
matters and I'm near ceiling with natural DNA.
