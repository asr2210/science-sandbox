# 025_wider_plus_paired_neg

## Design
5K cCREs x 5 WIDER tiles (+/-400bp, positives)
+ 5K non-cCRE genomic regions x 5 narrow tiles (negatives)
= 50K. Stack of 020 (wider) and 024 (paired neg) levers.

## Result
                eval_01  K562    HepG2   SKNSH
020 wider:      0.3216   0.144   0.200   0.621
024 paired neg: 0.3206   0.148   0.201   0.613
025 stacked:    0.3195   0.144   0.204   0.610

HepG2 NEW HIGH (0.204). K562 lost the 024 bump (0.144).
SKNSH dropped further (0.610). Mean DOWN.

## Interpretation: the levers ANTI-stack
The two levers don't add. Capacity is partitioned:
- Adding paired-neg moves capacity to "is this functional" discrim
- Adding wider positives moves capacity to "what is in flanking"
- Stacking spends capacity on both, neither head benefits more,
  and SKNSH (the dominant signal) is starved.

Specifically:
- HepG2 head benefits from EITHER context breadth OR functional
  contrast — capped at ~0.204.
- K562 head benefits ONLY from functional contrast; when positives
  are wider, the contrast signal is muddied (some positive tiles
  are 400bp away from cCRE core, edge of negative distribution).
- SKNSH head needs cCRE coverage diversity — both interventions
  reduce its effective cCRE training signal.

## Theory T17: capacity partitioning
The model has a fixed capacity that splits across the 3 cell-type
heads. Each head has its own "skill ceiling" that's lifted by
specific levers. Stacking levers can hurt heads whose levers
aren't included, by draining capacity.

The product of head ceilings sets the mean_r ceiling. To lift
mean_r we must either:
(a) Find a SINGLE intervention that lifts multiple heads, or
(b) Find an intervention that lifts one head a lot without
    hurting others (large net positive).

## Next
Experiment 026: dinuc-SHUFFLED cCRE negatives (matched
composition, no structure) instead of real genomic non-cCRE.
5K cCREs x 5 narrow + 5K dinuc-shuffled cCRE tiles x 5 = 50K.

Tests whether 024's K562 bump comes from:
(A) "real genomic non-cCRE context" (negatives in 024)
(B) "non-functional sequence in general" (shuffled would suffice)

Distinguishing matters because (A) means the negatives carry
useful intergenic context info; (B) means the contrast itself
(matched composition, no motif structure) is enough — a much
cheaper and more flexible lever.
