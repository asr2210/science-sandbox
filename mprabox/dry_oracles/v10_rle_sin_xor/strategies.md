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
| random_uniform                 | 0.5202 | 0.5203 | 0.5237 | 0.5245 | 0.5203 | 0.5217 | 0.5197 | 0.4672 | 0.5245 | 0.5152 | 0.5217 | 0.5237 | 0.5209 | 0.5202 |
| gc_50                          | 0.5176 | 0.5175 | 0.5193 | 0.5209 | 0.5175 | 0.5188 | 0.5178 | 0.4681 | 0.5209 | 0.5141 | 0.5188 | 0.5193 | 0.5210 | 0.5176 |
| gc_sweep                       | 0.4352 | 0.4353 | 0.4380 | 0.4296 | 0.4353 | 0.4377 | 0.4480 | 0.3990 | 0.4296 | 0.4348 | 0.4377 | 0.4380 | 0.4471 | 0.4352 |
| at_rich                        | 0.3930 | 0.3933 | 0.4031 | 0.3365 | 0.3933 | 0.3959 | 0.4358 | 0.3321 | 0.3365 | 0.3874 | 0.3959 | 0.4031 | 0.4316 | 0.3930 |
| alternating_ry                 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan |
| dirichlet_composition          | 0.3404 | 0.3406 | 0.3408 | 0.3327 | 0.3406 | 0.3420 | 0.3428 | 0.3332 | 0.3327 | 0.3405 | 0.3420 | 0.3408 | 0.3342 | 0.3404 |
| homopolymer_rich               | 0.2537 | 0.2541 | 0.2617 | 0.2412 | 0.2541 | 0.2544 | 0.2606 | 0.1259 | 0.2412 | 0.2293 | 0.2544 | 0.2617 | 0.2602 | 0.2537 |
| gc_rich                        | 0.2209 | 0.2205 | 0.2194 | 0.2718 | 0.2205 | 0.2233 | 0.1997 | 0.3139 | 0.2718 | 0.2562 | 0.2233 | 0.2194 | 0.2138 | 0.2209 |
| dinuc_repeat                   | 0.1785 | 0.1782 | 0.1786 | 0.1852 | 0.1782 | 0.1808 | 0.1845 | 0.2247 | 0.1852 | 0.1747 | 0.1808 | 0.1786 | 0.1806 | 0.1785 |
