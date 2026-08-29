# Experiment 020: Promoter-enriched library

## Plan
Filter cCREs to promoter-like (PLS, PLS,CTCF-bound, DNase-H3K4me3,
DNase-H3K4me3,CTCF-bound) = 66,812 elements. Sample 50k windows
centered on these with small jitter. Distinct from exp 005 (all 1M
cCREs) — focus on TSS-proximal regulatory rather than distal enhancers.

## Result
- eval_01 mean_r = **0.1301** — WORSE than random hg38 (~0.135)
- Roughly in line with cCRE (0.1285) and K562 DNase (0.1258)
- Promoter density does NOT help; any cCRE specialization hurts

## Implication
Confirmed for the third time: regulatory enrichment of any sort
underperforms uniform genome sampling. The test distribution is NOT
biased toward known regulatory elements.

## Theory consolidation (T17)
The test set behaves like uniform random hg38 windows, OR the model's
generalization curve is best fit by maximum-diversity training. Any
filter (chromatin, motif, complexity, cell-type, region-type) reduces
diversity and hurts.

## Next
Greedy k-mer coverage selection. Generate ~250k random candidate
windows, greedily pick 50k that maximize 6-mer (or 7-mer) coverage.
Tests whether selecting *for* diversity beats random sampling. If even
this doesn't beat 0.137, the ceiling is the ceiling.
