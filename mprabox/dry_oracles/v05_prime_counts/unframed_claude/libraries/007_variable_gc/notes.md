# Experiment 007 — Variable GC across library

## Hypothesis
chr22 has wide GC variance across regions. If that variance is the
lever, a synthetic library with per-seq GC ~ U(0.2, 0.8) should
match or beat chr22.

## Method
For each of 50K sequences: draw GC ~ U(0.2, 0.8), then iid base
sampling at that GC.

## Results
- eval_01: 0.0259 (chr22: 0.0492, random: 0.0420) → WORSE than BOTH
- Average: ~0.025
- Even worse than uniform 50% GC random

## Interpretation
Compositional variance across the library is NOT the lever. In fact
it HURT, because it includes many extreme-GC sequences that are
deeper into the bad part of the composition axis. Recall exp 5
showed 70% GC is bad; presumably 20% GC is similarly bad.

So chr22's advantage isn't compositional variance — it must be
the actual motif/repeat/dinucleotide content in real DNA.

## Theory update
T4 narrows: chr22's edge over random comes from non-compositional
features in real DNA (real motifs, real repeats, real dinucleotide
patterns). Synthetic variations of composition cannot match.

## Next
EXP 8: regulatory-enriched human sequences. Two paths:
1. Sample 200bp windows centered on chr22 CpG islands (UCSC track)
2. Download ENCODE cCREs from a small chromosome
Either way, denser regulatory content per sequence is the bet.
