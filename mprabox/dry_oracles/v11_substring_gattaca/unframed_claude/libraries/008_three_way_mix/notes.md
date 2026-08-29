# 008 — Three-way mix: 1/3 strict + 1/3 random + 1/3 motif

## Hypothesis
If multimodal beats unimodal (007), more modes might further improve mean_r.

## Setup
~16.7k strict 50ea + ~16.7k uniform random + ~16.7k motif-augmented.

## Result
- eval_01 mean=**0.8415** (K562 0.838, HepG2 0.810, SKNSH 0.877)
- Worse than 007 (0.878). HepG2 dropped from 0.911 to 0.810.

## Interpretation
"More modes" is not monotonic. The motif subset hurts HepG2 by too much,
dragging the joint. Lesson: only add modes that do not severely degrade any
cell line. Motif as currently designed is HepG2-hostile.

## Next
- 009: try a different second mode for hybrid — 25k Markov + 25k random.
  Tests whether the "two-mode lift" effect is generic to any pair of
  distinct designs, or specific to strict+random.
- 010+: explore ratio of strict/random, and add other non-motif modes.
