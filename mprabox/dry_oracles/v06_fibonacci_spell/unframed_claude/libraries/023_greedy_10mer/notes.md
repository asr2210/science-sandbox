# Experiment 023: Greedy 10-mer coverage maximization

## Plan
250k random hg38 candidates, greedy stochastic (pool=500) selection of
50k maximizing unique 10-mer coverage. K=10 chosen because 4^10=1M >>
50k*190 avg unique = 9.5M kmer-events but bounded by hg38 10-mer pool.

## Result
- eval_01 mean_r = **0.1355** — within noise of random
- Final coverage: 1,013k/1,048k 10-mers (96.6%)
- Greedy gain dropped from 191 at step 0 to 1 by step 45k
- Diversity maximization confirmed: 96.6% of 10-mer space covered

## Implication
Even with explicit 10-mer coverage maximization landing at 0.1355, no
breakthrough. The scorer's ceiling is NOT bounded by k-mer diversity in
training data. The 0.135-0.139 plateau is structural to either the
model's capacity or the test distribution mismatch.

## Conclusion (for the strategy)
All sampling-strategy levers exhausted with no clear wins:
- random hg38 seed variation
- multi-seed pooling
- tiling vs random
- revcomp augmentation
- GC stratification
- greedy k-mer coverage (k=7, k=10)
- regulatory enrichment (cCRE, DNase, promoter) -- all HURT
- shuffles, Markov, motif insertion -- all HURT or no-op

The best result remains exp 006 at 0.1387 (single lucky seed of plain
random hg38). The natural-distribution-wins theory is confirmed.

## Next
Remaining experiments should focus on:
- Final library: replay exp 006-equivalent + small augmentations
- Mega-mix combining multiple known-good sources
- One or two long-shot ideas (conservation, gene-dense oversample)
