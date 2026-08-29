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
| gc_sweep                       | 0.0039 | 0.0044 | 0.0037 | -0.0017 | 0.0044 | 0.0030 | -0.0014 | 0.0027 | -0.0017 | -0.0065 | 0.0030 | 0.0037 | 0.0109 | 0.0039 |
| homopolymer_rich               | 0.0021 | 0.0016 | 0.0001 | -0.0021 | 0.0016 | 0.0010 | 0.0032 | 0.0028 | -0.0021 | 0.0054 | 0.0010 | 0.0001 | -0.0007 | 0.0021 |
| dinuc_repeat                   | 0.0008 | 0.0000 | -0.0021 | -0.0006 | 0.0000 | -0.0016 | -0.0019 | 0.0020 | -0.0006 | 0.0020 | -0.0016 | -0.0021 | -0.0045 | 0.0008 |
| random_uniform                 | 0.0004 | 0.0003 | 0.0006 | -0.0018 | 0.0003 | 0.0006 | 0.0030 | -0.0020 | -0.0018 | 0.0073 | 0.0006 | 0.0006 | -0.0010 | 0.0004 |
| dirichlet_composition          | 0.0003 | -0.0002 | 0.0010 | -0.0026 | -0.0002 | 0.0002 | -0.0002 | 0.0034 | -0.0026 | -0.0008 | 0.0002 | 0.0010 | -0.0012 | 0.0003 |
| gc_rich                        | 0.0001 | -0.0000 | -0.0027 | 0.0020 | -0.0000 | -0.0002 | 0.0028 | 0.0004 | 0.0020 | 0.0003 | -0.0002 | -0.0027 | -0.0036 | 0.0001 |
| gc_50                          | -0.0006 | -0.0014 | 0.0014 | -0.0044 | -0.0014 | -0.0023 | 0.0013 | 0.0056 | -0.0044 | 0.0029 | -0.0023 | 0.0014 | -0.0003 | -0.0006 |
| alternating_ry                 | -0.0015 | -0.0017 | -0.0040 | 0.0005 | -0.0017 | -0.0006 | 0.0091 | -0.0026 | 0.0005 | -0.0001 | -0.0006 | -0.0040 | -0.0018 | -0.0015 |
| at_rich                        | -0.0032 | -0.0029 | -0.0034 | -0.0006 | -0.0029 | -0.0025 | -0.0047 | -0.0011 | -0.0006 | -0.0005 | -0.0025 | -0.0034 | -0.0014 | -0.0032 |
