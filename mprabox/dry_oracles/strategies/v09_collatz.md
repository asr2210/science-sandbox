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
| dirichlet_composition          | 0.2770 | 0.2771 | 0.2784 | 0.2346 | 0.2771 | 0.2766 | 0.2792 | 0.0679 | 0.2346 | 0.2536 | 0.2766 | 0.2784 | 0.2687 | 0.2770 |
| gc_sweep                       | 0.2766 | 0.2768 | 0.2780 | 0.2313 | 0.2768 | 0.2764 | 0.2786 | 0.0698 | 0.2313 | 0.2524 | 0.2764 | 0.2780 | 0.2715 | 0.2766 |
| gc_50                          | 0.2628 | 0.2632 | 0.2639 | 0.2401 | 0.2632 | 0.2620 | 0.2620 | 0.0814 | 0.2401 | 0.2568 | 0.2620 | 0.2639 | 0.2519 | 0.2628 |
| random_uniform                 | 0.2425 | 0.2425 | 0.2415 | 0.2300 | 0.2425 | 0.2417 | 0.2315 | 0.0909 | 0.2300 | 0.2430 | 0.2417 | 0.2415 | 0.2325 | 0.2425 |
| dinuc_repeat                   | 0.1911 | 0.1916 | 0.1938 | 0.1723 | 0.1916 | 0.1905 | 0.2014 | 0.0291 | 0.1723 | 0.1819 | 0.1905 | 0.1938 | 0.1964 | 0.1911 |
| homopolymer_rich               | 0.1628 | 0.1623 | 0.1561 | 0.1397 | 0.1623 | 0.1637 | 0.1457 | 0.0177 | 0.1397 | 0.1709 | 0.1637 | 0.1561 | 0.1423 | 0.1628 |
| at_rich                        | 0.1430 | 0.1430 | 0.1399 | 0.1532 | 0.1430 | 0.1430 | 0.1119 | 0.0584 | 0.1532 | 0.1275 | 0.1430 | 0.1399 | 0.1100 | 0.1430 |
| alternating_ry                 | 0.0859 | 0.0857 | 0.0743 | 0.0950 | 0.0857 | 0.0766 | 0.0497 | 0.0334 | 0.0950 | 0.0673 | 0.0766 | 0.0743 | 0.0483 | 0.0859 |
| gc_rich                        | -0.0367 | -0.0358 | -0.0292 | -0.0798 | -0.0358 | -0.0385 | 0.0228 | -0.0191 | -0.0798 | -0.0671 | -0.0385 | -0.0292 | 0.0217 | -0.0367 |
