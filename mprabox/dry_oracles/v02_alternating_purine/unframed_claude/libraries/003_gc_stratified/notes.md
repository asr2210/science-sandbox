# 003 gc_stratified

Each seq sampled with random target GC content from U(0.2, 0.8).

## Results
- eval_01: mean=0.1312 (vs 0.1342 baseline) — essentially flat
- SKNSH slightly down (0.379 vs 0.382)
- K562 slightly down (0.007 vs 0.010)
- eval_07 K562 dropped to -0.033 (notable — this eval sensitive to GC distribution)

## Interpretation
GC content stratification doesn't unlock anything. The scorer seems robust to
marginal nucleotide composition variation. Eval_07 in particular punished
extreme-GC sequences. This narrows the search: signal probably isn't
GC-content-related.
