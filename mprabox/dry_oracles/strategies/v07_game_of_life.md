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
| gc_50                          | 0.3972 | 0.3978 | 0.3902 | 0.3995 | 0.3978 | 0.3946 | 0.3977 | 0.2718 | 0.3995 | 0.3701 | 0.3946 | 0.3902 | 0.4081 | 0.3972 |
| random_uniform                 | 0.3951 | 0.3957 | 0.3880 | 0.3959 | 0.3957 | 0.3919 | 0.3963 | 0.2757 | 0.3959 | 0.3689 | 0.3919 | 0.3880 | 0.4063 | 0.3951 |
| gc_sweep                       | 0.3560 | 0.3562 | 0.3496 | 0.3563 | 0.3562 | 0.3544 | 0.3614 | 0.2547 | 0.3563 | 0.3387 | 0.3544 | 0.3496 | 0.3737 | 0.3560 |
| dirichlet_composition          | 0.3424 | 0.3433 | 0.3346 | 0.3473 | 0.3433 | 0.3407 | 0.3554 | 0.2377 | 0.3473 | 0.3248 | 0.3407 | 0.3346 | 0.3716 | 0.3424 |
| at_rich                        | 0.2987 | 0.2991 | 0.2966 | 0.2670 | 0.2991 | 0.2974 | 0.3313 | 0.1982 | 0.2670 | 0.2824 | 0.2974 | 0.2966 | 0.3410 | 0.2987 |
| gc_rich                        | 0.2224 | 0.2221 | 0.2167 | 0.2493 | 0.2221 | 0.2235 | 0.1950 | 0.2017 | 0.2493 | 0.2339 | 0.2235 | 0.2167 | 0.2170 | 0.2224 |
| homopolymer_rich               | 0.1748 | 0.1751 | 0.1731 | 0.1777 | 0.1751 | 0.1743 | 0.1770 | 0.0940 | 0.1777 | 0.1526 | 0.1743 | 0.1731 | 0.1858 | 0.1748 |
| alternating_ry                 | 0.1169 | 0.1170 | 0.1173 | 0.1101 | 0.1170 | 0.1127 | 0.1080 | 0.0805 | 0.1101 | 0.1082 | 0.1127 | 0.1173 | 0.1125 | 0.1169 |
| dinuc_repeat                   | -0.0306 | -0.0304 | -0.0263 | -0.0396 | -0.0304 | -0.0233 | -0.0202 | -0.0270 | -0.0396 | -0.0379 | -0.0233 | -0.0263 | -0.0219 | -0.0306 |
