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
| dirichlet_composition          | 0.0414 | 0.0416 | 0.0406 | 0.0472 | 0.0416 | 0.0412 | 0.0252 | 0.1056 | 0.0472 | 0.0302 | 0.0412 | 0.0406 | 0.0190 | 0.0414 |
| random_uniform                 | 0.0399 | 0.0401 | 0.0390 | 0.0464 | 0.0401 | 0.0398 | 0.0236 | 0.1214 | 0.0464 | 0.0300 | 0.0398 | 0.0390 | 0.0179 | 0.0399 |
| gc_50                          | 0.0397 | 0.0400 | 0.0395 | 0.0460 | 0.0400 | 0.0401 | 0.0248 | 0.1219 | 0.0460 | 0.0304 | 0.0401 | 0.0395 | 0.0203 | 0.0397 |
| at_rich                        | 0.0317 | 0.0317 | 0.0317 | 0.0326 | 0.0317 | 0.0319 | 0.0186 | 0.0918 | 0.0326 | 0.0182 | 0.0319 | 0.0317 | 0.0102 | 0.0317 |
| gc_rich                        | 0.0310 | 0.0313 | 0.0313 | 0.0322 | 0.0313 | 0.0310 | 0.0249 | 0.0813 | 0.0322 | 0.0317 | 0.0310 | 0.0313 | 0.0195 | 0.0310 |
| gc_sweep                       | 0.0275 | 0.0276 | 0.0268 | 0.0314 | 0.0276 | 0.0281 | 0.0113 | 0.0641 | 0.0314 | 0.0245 | 0.0281 | 0.0268 | 0.0095 | 0.0275 |
| homopolymer_rich               | 0.0210 | 0.0214 | 0.0190 | 0.0196 | 0.0214 | 0.0222 | 0.0110 | 0.0408 | 0.0196 | 0.0194 | 0.0222 | 0.0190 | 0.0045 | 0.0210 |
| alternating_ry                 | 0.0097 | 0.0097 | 0.0092 | 0.0134 | 0.0097 | 0.0072 | 0.0059 | 0.0338 | 0.0134 | 0.0062 | 0.0072 | 0.0092 | 0.0119 | 0.0097 |
| dinuc_repeat                   | -0.0301 | -0.0302 | -0.0286 | -0.0324 | -0.0302 | -0.0293 | -0.0139 | -0.1021 | -0.0324 | -0.0186 | -0.0293 | -0.0286 | -0.0094 | -0.0301 |
