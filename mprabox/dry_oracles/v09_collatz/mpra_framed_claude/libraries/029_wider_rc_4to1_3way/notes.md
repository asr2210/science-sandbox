# 029_wider_rc_4to1_3way

## Design
5K cCREs x 4 WIDER tiles + each tile's RC = 40K positives
+ 2.5K non-cCRE x 4 narrow = 10K negatives
= 50K (4:1 ratio).

3-way stack: wider + RC + paired neg.

## Result
                eval_01  K562    HepG2   SKNSH
020 wider:      0.3216   0.144   0.200   0.621
021 wider+RC:   0.3222   0.145   0.200   0.622
028 wider+neg:  0.3229   0.148   0.203   0.618  <- prev high
029 (3-way):    0.3216   0.143   0.203   0.619

RC stack FAILED. eval_01 dropped -0.0013 vs 028. K562 lost its
bump (0.148 -> 0.143). HepG2 and SKNSH unchanged.

## Interpretation: RC competes with paired neg for K562 capacity
Each cCRE now contributes 4 forward + 4 RC = 8 tile-instances
that are NOT independent training examples. The model's effective
unique positive diversity halved. The paired-neg contrast signal
needs distinct positive instances to learn against, so RC dilution
weakens the K562 bump.

RC and paired-neg are NOT orthogonal: both consume the discrim-
ination capacity. RC was free on top of wider alone (021) because
wider didn't use discrimination capacity.

## Theory T20: 4 lever-axes, 2 capacity pools
The 4 levers cluster into 2 mutually-exclusive capacity pools:
- "Identity / context" pool: wider tiles, RC.
  Lifts HepG2 + SKNSH.
- "Discrimination" pool: paired neg.
  Lifts K562 + HepG2.
HepG2 benefits from either pool; K562 needs discrim; SKNSH needs
identity. Mixing within a pool (wider+RC) is fine. Mixing across
(wider+neg) works at low neg fraction. Adding RC on top of
wider+neg consumes discrimination capacity needed for the K562
bump.

## Next
Experiment 030: HARD negatives (adjacent flanking, 200-1500bp
from cCRE midpoint instead of >2kb). Tests whether finer
discrimination boundary helps K562 further. If 030 > 028, the
K562 bump scales with negative difficulty. Final experiment in
the budget.
