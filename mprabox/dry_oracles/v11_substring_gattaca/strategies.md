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
| gc_50                          | 0.8591 | 0.8591 | 0.8530 | 0.8667 | 0.8591 | 0.8610 | 0.7939 | 0.7729 | 0.8667 | 0.8109 | 0.8610 | 0.8530 | 0.8220 | 0.8591 |
| random_uniform                 | 0.8566 | 0.8566 | 0.8508 | 0.8631 | 0.8566 | 0.8581 | 0.7920 | 0.7726 | 0.8631 | 0.8088 | 0.8581 | 0.8508 | 0.8213 | 0.8566 |
| gc_sweep                       | 0.8185 | 0.8187 | 0.8145 | 0.8218 | 0.8187 | 0.8185 | 0.7843 | 0.7670 | 0.8218 | 0.7714 | 0.8185 | 0.8145 | 0.7953 | 0.8185 |
| gc_rich                        | 0.7325 | 0.7331 | 0.7383 | 0.6980 | 0.7331 | 0.7342 | 0.7416 | 0.5608 | 0.6980 | 0.6629 | 0.7342 | 0.7383 | 0.7458 | 0.7325 |
| at_rich                        | 0.6779 | 0.6776 | 0.6679 | 0.7112 | 0.6776 | 0.6809 | 0.6127 | 0.6305 | 0.7112 | 0.6232 | 0.6809 | 0.6679 | 0.6155 | 0.6779 |
| homopolymer_rich               | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan |
| alternating_ry                 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan |
| dinuc_repeat                   | 0.7836 | 0.7834 | 0.7624 | 0.7983 | 0.7834 | 0.7822 | 0.6689 | 0.7258 | 0.7983 | 0.7145 | 0.7822 | 0.7624 | 0.6912 | 0.7836 |
| dirichlet_composition          | 0.6751 | 0.6753 | 0.6680 | 0.6847 | 0.6753 | 0.6756 | 0.6327 | 0.6542 | 0.6847 | 0.6409 | 0.6756 | 0.6680 | 0.6534 | 0.6751 |
