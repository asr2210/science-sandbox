# Experiment 021: Greedy 7-mer coverage maximization

## Plan
Sample 250k random hg38 candidates, greedily pick 50k that maximize
unique 7-mer set (4^7=16,384 possible). Stochastic greedy: per step
sample 1000 candidates, take the one with max new k-mer gain.

## Result
- eval_01 mean_r = **0.1363** — within noise of random hg38 (~0.135)
- 7-mer space (16k) saturated within first ~5k picks — remaining 45k were
  ~random within candidate pool. So greedy didn't really get to operate.

## Implication
At k=7, the space is too small to differentiate windows; greedy collapses
to random after a few thousand. To meaningfully exercise k-mer coverage
need k=10+ (4^10=1M, comparable to 50k*190 = 9.5M k-mer-events).

But: even if greedy at higher k did meaningfully differentiate, the
0.135 plateau suggests the scorer doesn't care about k-mer coverage —
it cares about distributional match.

## Next
Try GC-stratified random: uniformly sample windows from GC=30-70% buckets
instead of natural-weighted. Will MOVE the distribution rather than just
diversify within it. Tests whether peaked-GC (natural) or flat-GC helps.
