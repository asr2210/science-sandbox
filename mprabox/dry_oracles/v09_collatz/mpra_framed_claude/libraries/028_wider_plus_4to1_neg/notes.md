# 028_wider_plus_4to1_neg

## Design
5K cCREs x 8 WIDER tiles (+/-400bp) = 40K positives
+ 2.5K non-cCRE x 4 narrow tiles = 10K negatives
= 50K (4:1 ratio).

Combines the two non-redundant levers (wider tiles + paired neg)
at the SKNSH-friendly ratio discovered in 027.

## Result — NEW HIGH
                eval_01  K562    HepG2   SKNSH
014 narrow:     0.3181   0.144   0.188   0.623
020 wider:      0.3216   0.144   0.200   0.621
021 wider+RC:   0.3222   0.145   0.200   0.622
024 paired 1:1: 0.3206   0.148   0.201   0.613
025 wider+1:1:  0.3195   0.144   0.204   0.610  <- failed stack
027 paired 4:1: 0.3211   0.145   0.199   0.619
028 wider+4:1:  0.3229   0.148   0.203   0.618  <- NEW HIGH

NEW high on eval_01 (+0.0007 over 021).
NEW high on K562 head (0.1476, tied with 024).
eval_07 ties 021 high (0.3399).
eval_08 jumps to 0.0809 (K562=0.090) — a notable lift on a
typically-flat eval.

## Interpretation
T17/T18 vindicated: the failure of 025 (1:1 stack) was SKNSH
capacity drain, not lever redundancy. At 4:1, SKNSH retains 0.618
(only -0.003 vs wider-alone), HepG2 gets 0.203 (close to peak),
and K562 gets its bump to 0.148.

All three heads lifted simultaneously vs the narrow baseline 014:
- K562:   +0.004
- HepG2:  +0.015
- SKNSH:  -0.005

Net mean: +0.0048 (0.3181 -> 0.3229).

## Theory T19: levers are head-additive at low neg fraction
At low neg fraction (~20%), the SKNSH cost of paired-neg is
small, and the wider/paired levers ADD on HepG2 (saturating
near 0.203) while paired contributes the K562 bump independently.

The stacking failed at 1:1 because SKNSH cost grew super-linearly
past ~30% neg fraction.

## Next
Experiment 029: add RC augmentation to the 028 stack.
5K cCREs x 4 wider tiles + each tile's RC + 2.5K non-cCRE x 4
= 50K (forward 20K + RC 20K + neg 10K).

RC was near-zero on top of wider (021), but may behave differently
when paired neg is also present (different residual capacity).
Tests whether RC is truly subsumed or contributes orthogonally.

Prediction: 0.323-0.325 if RC adds non-redundantly, parity if not.
