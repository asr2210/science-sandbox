# 001_uniform_random — notes

## Design
50,000 sequences x 200 bp, each base sampled i.i.d. uniform from {A,C,G,T}.
No biology, no GC bias, no motif content. Establishes the floor.

## Hypothesis
A model trained on pure random DNA + measured activity should generalize
poorly. Predicted eval_01 mean_r ≪ 0.5.

## Result
- eval_01 mean_r = **0.6954** (k562=0.693, hepg2=0.687, sknsh=0.707)
- Range across 14 evals: 0.6553 (eval_12) to 0.8115 (eval_09).
- Per-cell-type pattern: SKNSH > K562 > HepG2 in essentially every eval.
- Seed-to-seed variability tiny (eval_01: 0.6917 / 0.6969 / 0.6976).
  → 3 seeds at 50K is plenty for stable scoring.
- Wall time: 914 s (~15 min).

## Interpretation
The "floor" is much higher than I predicted. Pure random DNA already gives
mean correlations of 0.66–0.81 across evals. This rules out the naive view
that the eval sets test specific learned regulatory grammar that random
DNA cannot supply. Possible explanations (to be tested):

1. **The model has strong inductive biases** — even on random training
   sequences, the model learns generic features (k-mer composition, GC,
   weak proto-motifs that occur by chance) that correlate with activity
   in the eval sets.
2. **The eval sets are dominated by trivially predictable features**
   (e.g., GC, dinucleotide composition, length) and only the headroom
   above ~0.70 reflects "real" regulatory grammar.
3. **The MPRA assay itself produces activity that is heavily driven by
   composition** — the readout has a strong baseline signal from generic
   sequence properties.

Cross-eval pattern is highly informative:
- eval_01 ≈ eval_05 (0.6954 vs 0.6951) — almost identical, strongly
  suggests they are the same or paired set
- eval_02, 06, 14 cluster at ~0.785 — likely a related family
- eval_09 highest (0.81), eval_12 lowest (0.66) — different headroom

Cell-type pattern (SKNSH > K562 > HepG2) is consistent across all evals,
which suggests it reflects assay-level differences (dynamic range, noise)
rather than library-specific biology.

## What this changes
- Floor for any structured library ≈ eval_01 = 0.70.
  Anything that doesn't clear this is uninformative or actively harmful.
- The interesting headroom is small in absolute terms but possibly large
  in relative terms — going from 0.70 to 0.80 is meaningful.
- I need to determine whether the floor is from generic composition or
  from the model's inductive bias.

## Next experiment idea
A library of natural human regulatory sequences (e.g., ENCODE cCREs).
This tests whether biological grammar adds anything over random. If
yes → biology matters, lean into it. If no → eval is composition-driven
and we need a very different strategy.
