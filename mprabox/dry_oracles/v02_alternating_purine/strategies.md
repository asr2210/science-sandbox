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
| random_uniform                 | 0.1264 | 0.1274 | 0.1392 | 0.1276 | 0.1274 | 0.1343 | 0.1365 | 0.0529 | 0.1276 | 0.1327 | 0.1343 | 0.1392 | 0.1250 | 0.1264 |
| gc_50                          | 0.1212 | 0.1213 | 0.1336 | 0.1102 | 0.1213 | 0.1385 | 0.1383 | 0.0595 | 0.1102 | 0.1303 | 0.1385 | 0.1336 | 0.1187 | 0.1212 |
| at_rich                        | 0.1023 | 0.1027 | 0.1213 | 0.0713 | 0.1027 | 0.1447 | 0.1323 | 0.0360 | 0.0713 | 0.0868 | 0.1447 | 0.1213 | 0.1183 | 0.1023 |
| gc_sweep                       | 0.1005 | 0.1003 | 0.1138 | 0.0874 | 0.1003 | 0.1169 | 0.1422 | 0.0534 | 0.0874 | 0.1154 | 0.1169 | 0.1138 | 0.1209 | 0.1005 |
| gc_rich                        | 0.0602 | 0.0603 | 0.0669 | 0.0796 | 0.0603 | 0.0592 | 0.0568 | 0.0389 | 0.0796 | 0.0786 | 0.0592 | 0.0669 | 0.0457 | 0.0602 |
| homopolymer_rich               | 0.0104 | 0.0103 | 0.0103 | 0.0161 | 0.0103 | 0.0100 | 0.0055 | 0.0043 | 0.0161 | 0.0148 | 0.0100 | 0.0103 | 0.0154 | 0.0104 |
| alternating_ry                 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan |
| dinuc_repeat                   | 0.1161 | 0.1168 | 0.1334 | 0.1106 | 0.1168 | 0.1340 | 0.1431 | 0.0230 | 0.1106 | 0.1341 | 0.1340 | 0.1334 | 0.1387 | 0.1161 |
| dirichlet_composition          | 0.1009 | 0.1015 | 0.1145 | 0.0973 | 0.1015 | 0.1117 | 0.1261 | 0.0397 | 0.0973 | 0.1317 | 0.1117 | 0.1145 | 0.1126 | 0.1009 |
