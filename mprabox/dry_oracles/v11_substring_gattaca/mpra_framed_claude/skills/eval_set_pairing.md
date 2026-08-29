# Eval set pairing observed

prepare.py returns 14 eval sets but several are exact duplicates across
experiments (or at least appear so on experiment 001). Pairs observed with
identical mean_r / k562_r / hepg2_r / sknsh_r down to 4 decimal places:

| pair      | exp 001 mean_r |
|-----------|----------------|
| 01 ↔ 14   | 0.8620         |
| 02 ↔ 05   | 0.8619         |
| 03 ↔ 12   | 0.8565         |
| 04 ↔ 09   | 0.8670         |
| 06 ↔ 11   | 0.8639         |
| 07        | 0.8062         |
| 08        | 0.7755         |
| 10        | 0.8122         |
| 13        | 0.8313         |

So there are effectively ≤ 9 unique evals. Treat each pair as one signal source.

When comparing experiments, the *unpaired* evals (07, 08, 10, 13) are where
random uniform fails most (especially in K562) — these are likely the most
sensitive tests of whether a library teaches real motif/syntax grammar.

Re-verify on each experiment in case the pairing is not stable across libraries.
