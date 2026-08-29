# 002_genomic_random_windows

50,000 random 200bp windows from GRCh38 chrs {1, 11, 19, 20, 21, 22}.
Reject N. Random strand. Seed 42.

## Result
mean across 14 evals: 0.524 (vs 0.342 for random — big jump)
eval_01: 0.4967 (vs 0.3425; +0.154)
Easiest: eval_07 (0.599), eval_13 (0.602), eval_10 (0.548)
Hardest: eval_08 (0.097, slightly WORSE than random's 0.110)

## Per-eval delta vs random baseline (positive = genomic better)
- eval_01: +0.154
- eval_02: +0.155
- eval_03: +0.169
- eval_04: +0.211  (biggest lift)
- eval_06: +0.168
- eval_07: +0.149
- eval_08: -0.012  (the only regression)
- eval_10: +0.146
- eval_13: +0.168

## Observations
1. Real genomic sequences are dramatically more informative than uniform
   random for nearly every eval set. ~0.15-0.20 lift across the board.
2. **eval_08 is anomalous**: random did *better*. Hypothesis: eval_08
   contains synthetic/random/non-human sequences that don't share genomic
   composition. Or sequences with very different motif content.
3. K562 == HepG2 again across all evals to 4 decimals. Either the eval
   harness collapses these, or this is a robust artifact across library
   types. Strong evidence the "3 cell types" are effectively 2 distinct
   signals + 1 paired.
4. SKNSH is consistently a hair higher than K562/HepG2 — about +0.01 to
   +0.02. Some cell-type specificity exists.
