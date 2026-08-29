# Exp 019 — HepG2 H3K27ac active enhancer peaks

50k 200bp windows centered (±100bp jitter) on HepG2 H3K27ac narrowPeak
summits (ENCFF580KMC, 41544 total; 7935 on our chroms).
GC mean=0.530, std=0.115.

## Result

| metric  | chr22 random | HepG2 H3K27ac |
|---------|-------------:|--------------:|
| eval_01 | 0.3202       | 0.3130        |
| k562    | 0.1443       | 0.1389        |
| hepg2   | 0.1990       | 0.1762        |
| sknsh   | 0.6173       | 0.6239        |

As predicted from DHS results: active enhancer peaks are GC-rich
(53%) so HepG2 drops (-0.023). SKNSH slightly up (+0.007) since
GC closer to SKNSH's 50% optimum.

Confirms: HepG2 score does NOT reward functional/annotated enhancers
— it rewards natural AT-balanced composition. Cell-type-specific
chromatin annotations are negative-correlated with our HepG2 score.

Useful finding: SKNSH likes ~50-53% GC more than chr22's 47% baseline.
Could maybe push SKNSH +0.01 with a slight GC enrichment.

**Idea for next**: chr22 random + extra GC-enriched sub-pool to boost
SKNSH without crashing HepG2.
