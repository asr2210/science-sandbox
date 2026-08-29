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
| dirichlet_composition          | 0.0768 | 0.0751 | 0.0967 | 0.0893 | 0.0751 | 0.0768 | 0.1460 | 0.0745 | 0.0893 | 0.1293 | 0.0768 | 0.0967 | 0.1453 | 0.0768 |
| random_uniform                 | 0.0711 | 0.0696 | 0.0888 | 0.0788 | 0.0696 | 0.0709 | 0.1330 | 0.0605 | 0.0788 | 0.1170 | 0.0709 | 0.0888 | 0.1326 | 0.0711 |
| gc_50                          | 0.0691 | 0.0673 | 0.0855 | 0.0816 | 0.0673 | 0.0690 | 0.1359 | 0.0576 | 0.0816 | 0.1162 | 0.0690 | 0.0855 | 0.1329 | 0.0691 |
| gc_sweep                       | 0.0643 | 0.0632 | 0.0844 | 0.0750 | 0.0632 | 0.0634 | 0.1320 | 0.0642 | 0.0750 | 0.1175 | 0.0634 | 0.0844 | 0.1330 | 0.0643 |
| gc_rich                        | 0.0581 | 0.0573 | 0.0694 | 0.0745 | 0.0573 | 0.0572 | 0.0962 | 0.0350 | 0.0745 | 0.1015 | 0.0572 | 0.0694 | 0.0996 | 0.0581 |
| homopolymer_rich               | 0.0570 | 0.0558 | 0.0800 | 0.0589 | 0.0558 | 0.0575 | 0.1032 | 0.0291 | 0.0589 | 0.0667 | 0.0575 | 0.0800 | 0.1013 | 0.0570 |
| at_rich                        | 0.0563 | 0.0551 | 0.0776 | 0.0563 | 0.0551 | 0.0579 | 0.1193 | 0.0588 | 0.0563 | 0.0987 | 0.0579 | 0.0776 | 0.1168 | 0.0563 |
| alternating_ry                 | 0.0076 | 0.0078 | 0.0111 | 0.0093 | 0.0078 | 0.0091 | 0.0036 | 0.0084 | 0.0093 | 0.0148 | 0.0091 | 0.0111 | 0.0168 | 0.0076 |
| dinuc_repeat                   | 0.0039 | 0.0038 | 0.0032 | 0.0087 | 0.0038 | 0.0037 | 0.0118 | 0.0021 | 0.0087 | 0.0033 | 0.0037 | 0.0032 | 0.0166 | 0.0039 |
