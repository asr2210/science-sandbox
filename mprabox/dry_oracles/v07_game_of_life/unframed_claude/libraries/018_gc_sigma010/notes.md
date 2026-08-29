# 018_gc_sigma010

## Hypothesis
Per-seq GC drawn from N(0.5, 0.10), clipped to [0.15, 0.85]. Maps upper edge of the per-seq GC plateau. 014 (σ=0.082, r=0.399) on plateau; 005 (σ=0.23, r=0.365) off plateau.

## Result
- **eval_01 mean_r = 0.3978** (K562=0.6167, HepG2=0.4343, SKNSH=0.1426)
- Still on plateau (within 0.001 of random uniform). Tiny dip from 014's 0.3989, well within noise.

## Interpretation
Plateau extends to GC σ=0.10. Boundary is somewhere between 0.10 and 0.23. We have a flat region of width ≈ 0.09 (from 0.010 to 0.10).

## Updated per-seq GC variance curve

| exp | per-seq GC std | eval_01 |
|---|---|---|
| 015 | 0.010 | 0.3975 |
| 001 | 0.035 | 0.3981 |
| 014 | 0.082 | **0.3989** ← highest |
| 018 | 0.106 | 0.3978 |
| 005 | 0.23 | 0.3647 |
| 004 | 0.30 | 0.3401 |

Plateau: r ≈ 0.397-0.399 for σ in [0.010, 0.10]. Outside that range, score drops smoothly.

## Next
Random uniform plateau is well-mapped. Need to test orthogonal levers:
- 019: CpG-enriched Markov (dinuc lever)
- 020+: explore other levers and try mix of "plateau variants" for submission
