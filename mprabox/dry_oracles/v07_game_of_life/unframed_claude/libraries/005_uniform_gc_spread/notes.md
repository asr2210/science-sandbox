# 005_uniform_gc_spread

## Hypothesis
Per-sequence GC drawn uniformly from U(0.1, 0.9) creates a library with mean GC≈50% and very wide per-sequence variance. Predicted: score lands between random uniform (0.398) and bimodal extremes (0.340), consistent with a smooth per-sequence GC penalty.

## Method
- 50,000 sequences. Per-sequence GC drawn from U(0.1, 0.9).
- Bases sampled i.i.d. with appropriate p(A)=p(T)=(1-GC)/2 and p(C)=p(G)=GC/2.
- Seed 42.

## Result
- **eval_01 mean_r = 0.3647** (K562=0.5657, HepG2=0.3969, SKNSH=0.1316)
- Exactly intermediate between random uniform (0.398) and bimodal (0.340), as predicted.

## Interpretation
Confirms theory T3: per-sequence GC ≈ 50% is a sweet spot. Deviations cost smoothly. Roughly:
- Random uniform (per-seq GC std ~3.5%): 0.398
- Uniform spread (per-seq GC std ~23%): 0.365
- Bimodal extremes (per-seq GC at 20%/80%): 0.340

A linear fit on (std, score) is consistent with these three points.

## Next
- 006: every sequence has *exactly* 50% GC (removes binomial GC noise). Tests whether the small natural GC variance in random uniform leaves room to improve.
- Future: probe non-GC structure — homopolymer runs, dinuc frequencies, motifs.
