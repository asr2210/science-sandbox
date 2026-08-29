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
| gc_50                          | 0.4243 | 0.4242 | 0.4228 | 0.4289 | 0.4242 | 0.4247 | 0.4231 | 0.3820 | 0.4289 | 0.4307 | 0.4247 | 0.4228 | 0.4211 | 0.4243 |
| random_uniform                 | 0.4228 | 0.4227 | 0.4212 | 0.4247 | 0.4227 | 0.4234 | 0.4288 | 0.3804 | 0.4247 | 0.4307 | 0.4234 | 0.4212 | 0.4193 | 0.4228 |
| at_rich                        | 0.3118 | 0.3118 | 0.3082 | 0.2749 | 0.3118 | 0.3112 | 0.3284 | 0.2654 | 0.2749 | 0.3181 | 0.3112 | 0.3082 | 0.3252 | 0.3118 |
| alternating_ry                 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan |
| dirichlet_composition          | 0.3478 | 0.3474 | 0.3460 | 0.3513 | 0.3474 | 0.3484 | 0.3468 | 0.2524 | 0.3513 | 0.3467 | 0.3484 | 0.3460 | 0.3478 | 0.3478 |
| gc_sweep                       | 0.3334 | 0.3336 | 0.3330 | 0.3216 | 0.3336 | 0.3327 | 0.3474 | 0.3093 | 0.3216 | 0.3426 | 0.3327 | 0.3330 | 0.3472 | 0.3334 |
| gc_rich                        | 0.2999 | 0.2995 | 0.2951 | 0.3201 | 0.2995 | 0.2982 | 0.2915 | 0.2625 | 0.3201 | 0.3007 | 0.2982 | 0.2951 | 0.2827 | 0.2999 |
| homopolymer_rich               | 0.1850 | 0.1852 | 0.1797 | 0.1814 | 0.1852 | 0.1845 | 0.1964 | 0.1016 | 0.1814 | 0.1890 | 0.1845 | 0.1797 | 0.1823 | 0.1850 |
| dinuc_repeat                   | 0.1079 | 0.1078 | 0.1056 | 0.1077 | 0.1078 | 0.1084 | 0.1077 | 0.1241 | 0.1077 | 0.1112 | 0.1084 | 0.1056 | 0.1116 | 0.1079 |
