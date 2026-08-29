# 019_dhs_70_30_gc_stratified_ccre_filtered

## What I tested
Stack 015 (GC-stratified 70/30, champion) with 008's cCRE-overlap
filter (restrict candidate DHS to those overlapping any ENCODE
cCRE class). Tests whether the orthogonal mechanisms add.

GC bin boundaries recomputed on the cCRE-overlapping subset
(1.35M of 3.59M DHS), which is GC-elevated relative to the full
pool. Per-bin counts (7K signal, 3K breadth) preserved at 015's
stability point.

## Result — biggest collapse yet
| metric   | 019    | 015    | 008    | 011    | Δ vs 015 |
|----------|--------|--------|--------|--------|----------|
| eval_01  | 0.7097 | 0.7509 | 0.7269 | 0.7383 | -0.041   |
| eval_07  | 0.7236 | 0.7986 | 0.7419 | 0.7751 | -0.075   |
| eval_08  | 0.6631 | 0.7270 | 0.7021 | 0.7041 | -0.064   |
| eval_13  | 0.7084 | 0.7897 | 0.7248 | 0.7644 | -0.081   |
| cross-14 | 0.7472 | 0.7960 | 0.7671 | 0.7811 | **-0.049** |

Per-seed eval_01: 0.7545 / 0.6975 / 0.6771 (std ≈ 0.040 — **widest
of any experiment yet**, even worse than 016/017/018's 0.022-0.027).

## Why stacking failed
Three mechanisms compound:

1. **Distribution shift**: cCRE-overlap restricts to enhancer/
   promoter elements that are systematically more GC-elevated
   than non-cCRE DHS. Recomputed GC bin boundaries on this subset
   give bin 0 = 0.020-0.390 (much narrower than 015's bin 0 =
   0.000-0.375 over the full pool). The "low-GC" bin is no longer
   sampling the same compositional space.

2. **Lost compositional diversity**: 015's win comes from forcing
   inclusion of low-GC distal-enhancer elements that are NOT in
   cCRE annotations (lower-confidence regulatory elements in
   heterochromatin-adjacent regions). Restricting to cCRE-overlap
   excludes exactly these elements, defeating the 015 mechanism.

3. **Subset stability**: per-bin counts of 7K/3K assume bin
   candidate pools >> per-bin draws. cCRE-restricted bin 1 has only
   250K candidates (vs 015's 685K), making per-seed draws less
   averageable and increasing variance. Hence the seed-level
   variance jump from 015's 0.017 to 019's 0.040.

## Theory update — v17 → v18
> **Orthogonal levers do NOT automatically stack.** When two
> levers act on the same underlying distribution, stacking them
> can produce a library that violates BOTH levers' assumptions
> (cCRE filter assumes "high-quality elements"; GC stratification
> assumes "diverse compositional coverage"; together they exclude
> the diverse low-quality elements that GC stratification needs).
>
> Compounding factors that broke this stack:
> 1. Filter restricts the support of the stratification axis.
> 2. The remaining-distribution shift changes the meaning of
>    quantile bins.
> 3. Smaller bin pools reduce per-seed averaging (variance).
>
> Practical rule: when stacking levers, ensure (a) the filter does
> not shift the stratification axis distribution, and (b) per-bin
> candidate pools remain large (>50K each).

## What's left to try
The "stack 015 with another orthogonal lever" path is much weaker
than expected. Three more useful directions:
- 020: bracket GC granularity at 3 bins (lower granularity, more
  per-bin counts) — tests if 5 was the unique sweet spot.
- 021: GC stratification with 100% signal-weighted (no breadth axis)
  — tests if the 70/30 mix is still needed when GC stratification
  is in play.
- 022+: try TF ChIP-seq density as a third axis from a truly
  independent assay.
