# 024_paired_random_genomic

## Design
5K cCREs x 5 narrow tiles (positives, +/-100bp)
+ 5K random non-cCRE genomic windows x 5 narrow tiles
  (negatives, midpoint >2kb from any cCRE midpoint)
= 50K. First library to include EXPLICIT non-cCRE genomic
negatives.

## Result
                eval_01  K562    HepG2   SKNSH   eval_07  eval_13
014 narrow:     0.3181   0.144   0.188   0.623   0.337    0.328
020 wider:      0.3216   0.144   0.200   0.621   0.338    0.331
024 paired:     0.3206   0.148   0.201   0.613   0.336    0.335 NEW

vs 014 narrow (same per-region tile config but +5K negatives):
  +0.0025 mean_r. HepG2 0.188 -> 0.201, K562 +0.004, SKNSH -0.010.
vs 020 wider (same total regions+tiles, different mechanism):
  -0.0010 mean_r. Comparable HepG2/K562, SKNSH slightly worse.

eval_13 NEW HIGH (0.335, prev 022 0.333).
K562 head moved from 0.144 -> 0.148 — first measurable lift on
K562 head in any library so far.

## Interpretation
Explicit pos/neg pairing recovers ~75% of the wider-tile lift on
HepG2 and adds an additional small but real lift on K562 (the
library-insensitive head). The wider-tile lift is therefore NOT
purely about pairing — wider tiles teach BOTH pairing-equivalent
discrimination AND something extra (positional/context inference
that 024 doesn't reproduce, since 024's positive tiles are narrow).

Two non-redundant skill axes now confirmed:
1. Context breadth (wider tiles)   -> HepG2 + SKNSH
2. Functional/non-functional contrast (paired neg) -> HepG2 + K562

If orthogonal, stacking gives a new high.

## Theory T16
- The eval-set mean_r is a mixture: SKNSH dominates (~0.62 ceiling),
  HepG2 (~0.20 ceiling), K562 (~0.145 ceiling), each moved by
  different levers.
- K562 head responds specifically to functional/non-functional
  contrast, not to context breadth alone. This is consistent with
  K562 being a transformed leukemia line with a more compact
  regulatory landscape: discrimination from non-regulatory DNA is
  the informative signal.
- HepG2 responds to both context AND contrast.
- SKNSH appears slightly worse with explicit non-cCRE negatives
  (the model spends capacity learning to reject non-cCRE which
  reduces capacity to model cCRE diversity for the head with the
  most signal).

## Next
Experiment 025: STACK wider positives + paired negatives.
5K cCREs x 5 WIDER (+/-400bp) tiles + 5K non-cCRE x 5 narrow tiles
= 50K. If the two skill axes are truly orthogonal, this should
push past 020/024 individually.

Prediction: eval_01 ~0.323-0.325 if stacked. ~0.320 if partial
redundancy. K562 stays at ~0.148, HepG2 at ~0.20+, SKNSH recovers
to ~0.62.
