# Experiment 015 — 30k motifs + 10k pELS + 10k dELS

## What I tested
Dropped motifs to 30k (just below the suspected threshold) and split
the remaining 20k between pELS (10k) and dELS (10k).

## Result — bad
- eval_07: mean=0.0057, K562=0.0140 (record K562 on eval_07)
- eval_08: mean=0.0064, K562=0.0107, HepG2=0.0061 (good but not record)
- eval_10/13: collapsed (lost dELS signal at 10k subset size)
- Most other evals NEGATIVE
- Mean across 14 ≈ -0.0011

## What this tells me
**The 30k motif threshold was too low too.** Even though we kept
motifs nearly full strength, the loss of HepG2/SKNSH baseline still
happened. 35k seems to be the right number; below it, broad signal
falls off a cliff.

Also: dELS at 10k did NOT preserve the eval_10/13 lift — confirming
that ~15k is needed per cCRE class.

## Updates to theory
**v3.7 → v3.8:** The motif-scaffold-to-real-cCRE ratio is *not*
freely tunable. 35k/15k is the sweet spot; 30k/20k loses on both
ends (motif too sparse to hold baseline, each cCRE class too sparse
to deliver signal).

This is a hard constraint of the 50k cap. We can't cover more than
~2 cell-type axes with cCRE classes.

## Next
Stop fighting the dilution constraint. Take the 012 recipe (35k +
15k pELS, our best mean library) and try to improve the MOTIF half
instead. Specifically: introduce homotypic motif clusters and TF-
pair syntax (e.g., GATA1+TAL1 paired for K562, HNF1+HNF4 paired for
HepG2). Real enhancers care about syntax/grammar, not just motif
counts.
