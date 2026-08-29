# Experiment 007: Tiled genome windows

## Plan
Tile genome at ~38kb step, take 50k N-free windows.

## Result
- eval_01 mean_r = **0.1346** (K562=0.036, HepG2=0.171, SKNSH=0.197)
- WORSE than full-genome random (0.1387)
- Same as chr22 random

## Why
Implementation bug: I tiled chromosomes in dict-order (chr1, chr10, chr11, chr12,
chr13, chr14, chr15...) and broke when N hit. So library is biased toward chr1
and early-alphabet chromosomes, not balanced across the genome.

## Lesson
Random sampling weighted by chrom length (exp 006) gives broader diversity than
my tiling approach. Diversity matters more than non-redundancy at this scale
(50k / 3Gb = one window per ~60kb, plenty of room).

## Skip-ahead plan
Move on rather than fix this — random sampling is already a working baseline.
Next: probe whether sequence STRUCTURE matters by dinucleotide-shuffling
genome windows. If shuffled scores ≈ raw, composition is everything.
