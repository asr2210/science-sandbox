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
| dirichlet_composition          | 0.3514 | 0.3521 | 0.3784 | 0.3347 | 0.3521 | 0.3621 | 0.4372 | 0.0770 | 0.3347 | 0.3727 | 0.3621 | 0.3784 | 0.4320 | 0.3514 |
| gc_50                          | 0.3209 | 0.3211 | 0.3469 | 0.3028 | 0.3211 | 0.3410 | 0.4181 | 0.1122 | 0.3028 | 0.3888 | 0.3410 | 0.3469 | 0.4132 | 0.3209 |
| random_uniform                 | 0.3187 | 0.3188 | 0.3453 | 0.2727 | 0.3188 | 0.3440 | 0.4363 | 0.1084 | 0.2727 | 0.3748 | 0.3440 | 0.3453 | 0.4109 | 0.3187 |
| dinuc_repeat                   | 0.3050 | 0.3058 | 0.3526 | 0.2865 | 0.3058 | 0.3575 | 0.4191 | 0.0941 | 0.2865 | 0.3922 | 0.3575 | 0.3526 | 0.4036 | 0.3050 |
| alternating_ry                 | 0.2641 | 0.2648 | 0.3033 | 0.2244 | 0.2648 | 0.3072 | 0.3885 | 0.0655 | 0.2244 | 0.3407 | 0.3072 | 0.3033 | 0.3713 | 0.2641 |
| gc_sweep                       | 0.2485 | 0.2483 | 0.2597 | 0.1604 | 0.2483 | 0.2580 | 0.4119 | 0.0527 | 0.1604 | 0.2076 | 0.2580 | 0.2597 | 0.3358 | 0.2485 |
| at_rich                        | 0.1911 | 0.1914 | 0.2051 | 0.0765 | 0.1914 | 0.1963 | 0.3936 | 0.0360 | 0.0765 | 0.1090 | 0.1963 | 0.2051 | 0.3115 | 0.1911 |
| gc_rich                        | 0.1514 | 0.1506 | 0.1547 | 0.1715 | 0.1506 | 0.1545 | 0.1218 | 0.0361 | 0.1715 | 0.2170 | 0.1545 | 0.1547 | 0.1539 | 0.1514 |
| homopolymer_rich               | 0.1436 | 0.1432 | 0.1373 | 0.1105 | 0.1432 | 0.1340 | 0.1751 | 0.0867 | 0.1105 | 0.1299 | 0.1340 | 0.1373 | 0.1513 | 0.1436 |
