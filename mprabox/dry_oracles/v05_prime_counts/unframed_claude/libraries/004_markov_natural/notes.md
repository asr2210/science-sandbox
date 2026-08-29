# Experiment 004 — Markov natural-like sequences

## Hypothesis
T2 predicted real-genome-like dinucleotide composition (AT-bias,
CpG depletion) puts sequences in-distribution for human-trained
models, raising r.

## Method
Order-2 Markov chain trained on approximate human dinucleotide
frequencies. Each 200bp sequence sampled independently.

## Results
- eval_01: -0.0052 (random was +0.0420) → DROPPED INTO NEGATIVE
- eval_08: -0.0149 (random was +0.1237) → DRAMATIC DROP
- HepG2 is consistently negative across all evals
- Average mean_r: ~-0.005

## Interpretation
T2 is WRONG. Natural-like composition hurts. Two important things:

1. The shift from random uniform to natural lowered r everywhere
   AND turned HepG2 negative. This suggests the oracle's models
   were NOT trained on natural human genomic DNA.

2. The biggest change: GC dropped from 50% to ~40%, and CpG
   dinucleotides dropped from ~6% to ~1% of the total. Either of
   these (or both) drove r down.

## Theory update — T3
The underlying scoring model is likely trained on **synthetic random
DNA libraries** (think MPRA where inserts are random 200-mers). In
that distribution, uniform random IS in-distribution, and natural
DNA is OUT-of-distribution. We get nonzero r on random uniform
because random is what the model expects; we get negative r on
natural because the composition shift creates systematic mismatches
between whatever the two correlated functions are computing.

Strong corollary: try compositional sweeps within the uniform-random
family. GC bias may push r further up.

## Next
EXP 5: 70% GC uniform random (P(G)=P(C)=0.35, P(A)=P(T)=0.15).
Tests if GC alone is the lever within the synthetic-random family.
