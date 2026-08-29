# Baseline Strategies


Performance of systematic baseline strategies evaluated before your run.
All used exactly 50,000 sequences. Performance is Pearson r (mean_r).


## Strategy Descriptions

**random_uniform** — Fully random sequences, each base equally likely.

**gc_sweep** — GC content linearly swept from 0% to 100% across sequences.

**gc_50** — All sequences at 50% GC content.

**at_rich** — 80% AT, 20% GC — biased toward A and T.

**gc_rich** — 80% GC, 20% AT — biased toward G and C.

**homopolymer_rich** — Sequences with long runs of the same base (geometric run lengths).

**alternating_ry** — Strict alternation of purines and pyrimidines (RYRYRY...).

**dinuc_repeat** — Dinucleotide repeats (e.g., ACACAC...) with small random patches.

**dirichlet_composition** — Each sequence draws base frequencies from a Dirichlet prior — diverse compositions.


---


## Results


| strategy | eval_01 | eval_02 | eval_03 | eval_04 | eval_05 | eval_06 | eval_07 | eval_08 | eval_09 | eval_10 | eval_11 | eval_12 | eval_13 | eval_14 |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| dirichlet_composition          | 0.1383 | 0.1387 | 0.1373 | 0.1340 | 0.1387 | 0.1388 | 0.1296 | 0.0641 | 0.1340 | 0.1232 | 0.1388 | 0.1373 | 0.1300 | 0.1383 |
| gc_sweep                       | 0.1191 | 0.1194 | 0.1177 | 0.1173 | 0.1194 | 0.1206 | 0.1075 | 0.0607 | 0.1173 | 0.1092 | 0.1206 | 0.1177 | 0.1189 | 0.1191 |
| gc_50                          | 0.1180 | 0.1180 | 0.1182 | 0.1138 | 0.1180 | 0.1193 | 0.1089 | 0.0532 | 0.1138 | 0.1060 | 0.1193 | 0.1182 | 0.1125 | 0.1180 |
| random_uniform                 | 0.1158 | 0.1157 | 0.1158 | 0.1167 | 0.1157 | 0.1176 | 0.1108 | 0.0564 | 0.1167 | 0.1143 | 0.1176 | 0.1158 | 0.1155 | 0.1158 |
| at_rich                        | 0.1062 | 0.1063 | 0.1053 | 0.0976 | 0.1063 | 0.1061 | 0.1073 | 0.0442 | 0.0976 | 0.1004 | 0.1061 | 0.1053 | 0.1123 | 0.1062 |
| gc_rich                        | 0.0589 | 0.0585 | 0.0549 | 0.0676 | 0.0585 | 0.0596 | 0.0398 | 0.0367 | 0.0676 | 0.0603 | 0.0596 | 0.0549 | 0.0407 | 0.0589 |
| homopolymer_rich               | 0.0582 | 0.0583 | 0.0596 | 0.0606 | 0.0583 | 0.0596 | 0.0505 | 0.0131 | 0.0606 | 0.0498 | 0.0596 | 0.0596 | 0.0613 | 0.0582 |
| alternating_ry                 | 0.0333 | 0.0339 | 0.0368 | 0.0418 | 0.0339 | 0.0340 | 0.0327 | 0.0077 | 0.0418 | 0.0334 | 0.0340 | 0.0368 | 0.0334 | 0.0333 |
| dinuc_repeat                   | 0.0221 | 0.0220 | 0.0276 | 0.0360 | 0.0220 | 0.0230 | 0.0254 | 0.0080 | 0.0360 | 0.0317 | 0.0230 | 0.0276 | 0.0323 | 0.0221 |
