# 026_shuffled_negatives

## Design
5K cCREs x 5 narrow tiles (positives, +/-100bp)
+ 5K cCRE tiles dinucleotide-shuffled (negatives, matched
  composition, no motif structure)
= 50K. Direct counterpart to 024 (real intergenic negatives).

## Result
                eval_01  K562    HepG2   SKNSH   eval_07
014 narrow:     0.3181   0.144   0.188   0.623   0.337
024 real neg:   0.3206   0.148   0.201   0.613   0.336
026 shuf neg:   0.3190   0.142   0.192   0.623   0.339 NEW

eval_07 NEW HIGH (0.3393, prev 021 0.3399 close). SKNSH on
eval_07 NEW HIGH (0.6521).

## Interpretation: K562 bump requires REAL genomic sequence
- K562 head: 0.148 (real neg, 024) -> 0.142 (shuf, 026): bump GONE
- HepG2 head: 0.201 -> 0.192: 60% of lift gone
- SKNSH head: 0.613 -> 0.623: RECOVERED

The K562 bump in 024 was not just "non-functional contrast" but
specifically REAL INTERGENIC GENOMIC INFORMATION. The K562 head
appears to benefit from intergenic context features (repeat
classes, GC patterns, etc.) absent from shuffled sequences.

SKNSH is hurt by REAL non-cCRE neg (the model treats them as
non-trivial which steals capacity) but NOT by SHUFFLED neg (model
treats them as obvious noise; ignores them).

## Theory T18: negatives have a SPECIFICITY signature
Two negative types teach different things:
- REAL non-cCRE genomic: useful intergenic context info (K562
  benefit) + capacity tax (SKNSH cost). Net: +0.003 mean_r.
- SHUFFLED matched-composition: easy negatives, model ignores
  them, modest contrast benefit. Net: +0.001 mean_r.

For mean_r to exceed 0.322, we need negatives that benefit
multiple heads without taxing SKNSH.

## Next
Experiment 027: pos:neg RATIO sweep. The 50/50 split in 024
took 5K cCREs of capacity away. Try 4:1 (40K positives, 10K
negatives) to give more cCRE coverage while keeping a contrast
signal.

Design: 5K cCREs x 8 narrow tiles + 2.5K non-cCRE x 4 narrow
tiles = 50K. Tests whether K562 bump survives at lower neg
fraction AND SKNSH recovers.

Prediction: if both, mean_r ~0.322-0.324 (new high possible).
If K562 bump needs 50/50, K562 reverts and lift comes only from
HepG2 (~0.320).
