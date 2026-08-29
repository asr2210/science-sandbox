# 016_dhs_70_30_gc_stratified_10bins

## What I tested
015 with the GC granularity doubled: 10 equal-population deciles
instead of 5 quintiles. Per-bin counts halved (3.5K signal, 1.5K
breadth per bin). Tests whether finer GC control adds further lift
or crosses the stability floor we discovered in 012/013.

## Result — collapse below 015 (and below 011)
| metric   | 016    | 015 (champ) | 011    | Δ vs 015 |
|----------|--------|-------------|--------|----------|
| eval_01  | 0.7190 | 0.7509      | 0.7383 | -0.032   |
| eval_07  | 0.7534 | 0.7986      | 0.7751 | -0.045   |
| eval_08  | 0.6779 | 0.7270      | 0.7041 | -0.049   |
| eval_13  | 0.7456 | 0.7897      | 0.7644 | -0.044   |
| cross-14 | 0.7596 | 0.7960      | 0.7811 | **-0.036** |

Per-seed eval_01: 0.7352 / 0.7339 / 0.6879 (std ≈ 0.027 — wide,
matching 012/013 instability rather than 015).

## Why it collapsed
Per-bin counts in the breadth half are 1.5K — well below the
~12-15K stability floor we identified for the breadth axis in
012/013. With 10 narrow GC bins, the breadth half is split into
fragments too small to provide stable training signal. The seed=2
outlier (0.6879) is a model that landed in a much worse local
optimum because the GC-bin × breadth composition randomized
unfavorably.

So the per-axis stability floor is **per-(axis × bin)**, not just
per-axis. Stratification doesn't get the benefit of pooling counts
across bins — each (axis, bin) cell is its own independent draw
that needs its own minimum sample count.

## Theory update — v14 → v15
> Stratification has a per-cell stability floor analogous to the
> per-axis stability floor we discovered in 012/013. Each (axis,
> bin) cell needs ~3K+ elements to produce a stable training
> contribution. Below that, the per-seed library composition
> randomizes too much across bins and the optimization basin loses
> coherence.
>
> Stratified design budget = N_TARGET / (n_axes × n_bins). For
> 50K total split 70/30 across 2 axes: 5 bins gives 7K signal +
> 3K breadth per bin (both safe at 5 bins). 10 bins gives 3.5K
> signal + 1.5K breadth per bin (breadth crosses the floor).
>
> Practical rule: when adding stratification, budget
> floor(n_per_bin) ≥ 3K per axis-bin cell. With 50K total and 70/30
> split, this caps GC (or any single stratification) at 5 bins.

## Decision (executing committed rule)
016 < 015 by > 0.003 cross-14 → 5 GC bins is the optimum
granularity. 015 remains the new champion. Pivot to alternate
sequence-composition axes for 017.

## Next
- 017: CpG O/E stratified (5 bins). CpG O/E is correlated with GC
  but not identical — CpG islands vs CpG-depleted regions reflect
  a real regulatory distinction (promoter vs distal-enhancer). If
  CpG O/E independently lifts, the win mechanism is "any sequence-
  composition axis under-represented in the natural draw." If it
  doesn't lift on top of 011, GC specifically encodes the lever.
- 018: combine GC + CpG O/E joint stratification (if 017 is positive).
- 019: TF ChIP-seq density as a third axis if sequence axes plateau.
