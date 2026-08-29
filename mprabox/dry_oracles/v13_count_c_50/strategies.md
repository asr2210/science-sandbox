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
| gc_sweep                       | 0.4169 | 0.4162 | 0.4063 | 0.3867 | 0.4162 | 0.4163 | 0.4635 | 0.1790 | 0.3867 | 0.3937 | 0.4163 | 0.4063 | 0.4363 | 0.4169 |
| dirichlet_composition          | 0.3634 | 0.3634 | 0.3633 | 0.3673 | 0.3634 | 0.3676 | 0.3946 | 0.2114 | 0.3673 | 0.3695 | 0.3676 | 0.3633 | 0.3830 | 0.3634 |
| at_rich                        | 0.2634 | 0.2639 | 0.2994 | -0.0432 | 0.2639 | 0.2702 | 0.5129 | -0.3262 | -0.0432 | 0.3115 | 0.2702 | 0.2994 | 0.4942 | 0.2634 |
| gc_rich                        | 0.2097 | 0.2085 | 0.1647 | 0.4084 | 0.2085 | 0.2038 | -0.0293 | 0.4348 | 0.4084 | 0.1241 | 0.2038 | 0.1647 | -0.0602 | 0.2097 |
| random_uniform                 | 0.1414 | 0.1402 | 0.0893 | 0.4061 | 0.1402 | 0.1309 | -0.1326 | 0.5786 | 0.4061 | 0.0974 | 0.1309 | 0.0893 | -0.1359 | 0.1414 |
| gc_50                          | 0.1108 | 0.1093 | 0.0588 | 0.3883 | 0.1093 | 0.1012 | -0.1649 | 0.5808 | 0.3883 | 0.0784 | 0.1012 | 0.0588 | -0.1668 | 0.1108 |
| homopolymer_rich               | 0.0620 | 0.0622 | 0.0679 | -0.0037 | 0.0622 | 0.0581 | 0.1259 | 0.0011 | -0.0037 | 0.0566 | 0.0581 | 0.0679 | 0.1030 | 0.0620 |
| dinuc_repeat                   | 0.0319 | 0.0328 | 0.0674 | -0.1161 | 0.0328 | 0.0350 | 0.1654 | -0.3289 | -0.1161 | 0.0560 | 0.0350 | 0.0674 | 0.1613 | 0.0319 |
| alternating_ry                 | 0.0261 | 0.0260 | 0.0078 | 0.0905 | 0.0260 | 0.0153 | -0.0519 | 0.1332 | 0.0905 | 0.0204 | 0.0153 | 0.0078 | -0.0385 | 0.0261 |
