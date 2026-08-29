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
| gc_sweep                       | 0.6014 | 0.6014 | 0.5991 | 0.5132 | 0.6014 | 0.5998 | 0.6673 | 0.1226 | 0.5132 | 0.5923 | 0.5998 | 0.5991 | 0.6365 | 0.6014 |
| dirichlet_composition          | 0.5318 | 0.5321 | 0.5328 | 0.4760 | 0.5321 | 0.5320 | 0.5837 | 0.1686 | 0.4760 | 0.5159 | 0.5320 | 0.5328 | 0.5676 | 0.5318 |
| at_rich                        | 0.4959 | 0.4969 | 0.5154 | 0.1785 | 0.4969 | 0.4901 | 0.6592 | 0.0810 | 0.1785 | 0.5256 | 0.4901 | 0.5154 | 0.6327 | 0.4959 |
| random_uniform                 | 0.4940 | 0.4940 | 0.4972 | 0.4203 | 0.4940 | 0.4927 | 0.5461 | 0.1608 | 0.4203 | 0.4917 | 0.4927 | 0.4972 | 0.5263 | 0.4940 |
| gc_50                          | 0.4728 | 0.4725 | 0.4721 | 0.4250 | 0.4725 | 0.4704 | 0.5170 | 0.1605 | 0.4250 | 0.4700 | 0.4704 | 0.4721 | 0.4965 | 0.4728 |
| alternating_ry                 | 0.1594 | 0.1596 | 0.1587 | 0.1371 | 0.1596 | 0.1529 | 0.1636 | 0.0459 | 0.1371 | 0.1466 | 0.1529 | 0.1587 | 0.1573 | 0.1594 |
| dinuc_repeat                   | 0.1489 | 0.1491 | 0.1505 | 0.1409 | 0.1491 | 0.1491 | 0.1562 | 0.0570 | 0.1409 | 0.1332 | 0.1491 | 0.1505 | 0.1472 | 0.1489 |
| homopolymer_rich               | 0.0828 | 0.0820 | 0.0910 | 0.0477 | 0.0820 | 0.0818 | 0.1091 | 0.0224 | 0.0477 | 0.1131 | 0.0818 | 0.0910 | 0.0942 | 0.0828 |
| gc_rich                        | 0.0404 | 0.0378 | -0.0012 | 0.3059 | 0.0378 | 0.0474 | -0.2092 | 0.0891 | 0.3059 | 0.0543 | 0.0474 | -0.0012 | -0.1780 | 0.0404 |
