# Experiment 002 — Random hg38 genomic windows

## What I tested
50,000 random 200 bp windows sampled uniformly across hg38 autosomes
(weighted by chromosome length). Rejected windows containing N. Seed=2.

## Hypothesis
Real genomic sequences carry real motif grammar — the model should
learn much more than from uniform random DNA. Predicted big jump from
~0 to maybe 0.2–0.4.

## Result
- eval_01 = 0.0039 (vs 0.0012 for random DNA)
- Mean across 14 evals ≈ 0.002.
- Basically still at the floor. Walltime 29 s.

## What this tells me — BIG SURPRISE
Random genomic sampling does **not** beat random DNA in any meaningful
way. My theory was wrong about "realistic sequences = informative
library." Plausible explanations:

1. **The genome is mostly silent.** ~98% of 200 bp windows are
   non-regulatory. Their MPRA activity is essentially noise around a
   constant low value. With ~98% of training labels being uninformative,
   the model has nothing to latch onto. The signal is buried in label
   noise.
2. **Dynamic range, not realism, is what trains a model.** The
   informative training pairs are sequences with *meaningfully different*
   activity. A library of mostly-zero-activity sequences is mostly
   redundant from a learning perspective, regardless of how realistic
   the sequences are.
3. **The model needs positives.** A motif-recognizing CNN needs
   examples where the motif IS active. If your 50,000 sequences contain
   only 500 active enhancers (and 49,500 silent windows), you have a
   ~500-example training set in practice.

## Updates to theory
- **Coverage of *active* regulatory space matters far more than
  realism.** A library should target sequences likely to span a wide
  activity range. Random genomic sampling fails this because activity
  is sparse in the genome.
- Library design = active learning problem. We should bias toward
  sequences predicted (a priori, from annotations) to be active.

## Next
Experiment 003: enhancer/promoter-enriched library — sample from
ENCODE candidate cis-regulatory elements (cCRE) rather than the whole
genome. This should give a much higher density of active sequences.

If 003 beats 002 by a wide margin, the theory of "active sequences
matter" is supported. If not, something else is going on.
