# 010_multichrom_strat

## What
50K natural hg38 sequences from chr1, chr7, chr18, chr19, chr22 (varying chromosome compositions). GC-stratified into 40 bins on [0.18, 0.78].

## Why
Test if more diverse genomic source + wider stratification beats single-chromosome stratification.

## Results
eval_01: **0.5539** (vs 0.5562 exp 9 → -0.4%, no improvement)
- K562_r: 0.579 (vs 0.581)
- HepG2_r: 0.537 (vs 0.541)
- SKNSH_r: 0.546 (vs 0.546)

Essentially identical to exp 9.

## Interpretation
Adding more chromosomes did NOT add eval_01-relevant variance. The natural-stratified approach plateaus around 0.555. GC axis is exhausted.

## Plan
Need a new axis. Try inserting strong activator motifs into natural sequences — discrete biological signal on top of natural backbone might add agreement-friendly variance without breaking k-mer naturalness like it did in pure-random backgrounds.
