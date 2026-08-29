# 027_pos_neg_ratio_4to1

## Design
5K cCREs x 8 narrow tiles (40K positives)
+ 2.5K non-cCRE x 4 narrow tiles (10K negatives)
= 50K. Pos:neg = 4:1 (vs 024's 1:1).

## Result
                eval_01  K562    HepG2   SKNSH
014 narrow:     0.3181   0.144   0.188   0.623
020 wider:      0.3216   0.144   0.200   0.621
024 paired 1:1: 0.3206   0.148   0.201   0.613
027 4:1:        0.3211   0.145   0.199   0.619

4:1 ratio is a clean sweet spot:
- K562: small bump preserved (0.145, marginal vs baseline 0.144)
- HepG2: almost full lift (0.199 vs 024's 0.201)
- SKNSH: partly recovered (0.619 vs 0.623 baseline, vs 024's 0.613)

Mean: 0.3211 — better than 024's 0.3206 but below 020's 0.3216.

## Interpretation
The K562 bump is fragile — needed nearly the full 1:1 neg
fraction. At 4:1, most of K562 bump is gone (0.148 -> 0.145).
HepG2 lift is robust to ratio change. SKNSH recovers proportionally
to neg fraction reduction.

The "right" ratio is a per-head tradeoff with no single winner
under the narrow-positive design. To push past 0.322, must stack
with another non-redundant lever.

## Next
Experiment 028: WIDER positives + 4:1 neg ratio.
5K cCREs x 8 WIDER tiles (+/-400bp) + 2.5K non-cCRE x 4 narrow
= 50K. Tests whether wider+paired stacks WHEN SKNSH isn't drained
(unlike 025 which used 1:1 ratio and failed).

If 028 > 020 (0.3216), 4:1 ratio rescues the stacking and we may
hit new high. Prediction: 0.322 ± 0.003.
