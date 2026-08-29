# Experiment 001 — Random uniform DNA

## What I tested
50,000 sequences, 200 bp each, each base i.i.d. uniform from {A,C,G,T}.
Establishes the absolute floor: a library with **no biological signal
at all**. The model has nothing to learn except possibly batch/GC-style
biases.

## Hypothesis
Activity will be uniformly near zero across sequences. The trained model
will fail (r ≈ 0) on every eval set because there is no
sequence-activity relationship to learn.

## Result
- All 14 evals: |r| < 0.012. Mean across evals ≈ 0.001.
- eval_01 (primary) = 0.0012.
- Walltime: 27 s evaluation, 59 s total.

## What this tells me
1. **Floor confirmed at r ≈ 0.** Any future library must beat this by
   a wide margin.
2. **Some eval pairs return identical scores** (e.g. 02==05, 04==09,
   06==11, 03==12, 01==14). They are probably the same underlying
   dataset under different split/sampling. So I effectively have ~9
   distinct evals, not 14.
3. **Negative correlations are real noise.** SK-N-SH systematically
   gave slightly negative r across many evals — likely just noise from
   a small effective test set, not a signal.

## Updates to theory
No surprises — random DNA is uninformative. The interesting question
now is **how much** of a jump we get from real genomic sequence, and
how that compares to engineered-motif libraries.

## Next
Experiment 002: random 200 bp windows from hg38 autosomes. This
introduces real motif grammar, realistic GC/dinucleotide distributions,
and a realistic activity distribution (mostly low, occasional high).
This is the "boring but probably good" benchmark every subsequent
library must beat.
