# 021_dhs_70_30_gc_stratified_3bins

## What I tested
015 (champion) with N_BINS = 3 instead of 5. Same 70/30 mix,
identical draw plan, just coarser GC partitioning. Per-bin counts
(11.7K signal + 5K breadth) are well above the 3K stability floor
— the safest per-bin counts of any GC-stratified experiment so
far. Brackets the granularity question from the coarse side
(016 = 10 bins violates floor; 015 = 5 bins is champion).

## Result — falsification, big collapse
| metric   | 021    | 015    | 011    | 016    | 021 vs 015 | 021 vs 011 |
|----------|--------|--------|--------|--------|------------|------------|
| eval_01  | 0.7173 | 0.7509 | 0.7383 | 0.7190 | -0.034     | -0.021     |
| eval_07  | 0.7504 | 0.7986 | 0.7751 | 0.7534 | -0.048     | -0.025     |
| eval_08  | 0.6651 | 0.7270 | 0.7041 | 0.6779 | -0.062     | -0.039     |
| eval_13  | 0.7409 | 0.7897 | 0.7644 | 0.7456 | -0.049     | -0.024     |
| cross-14 | 0.7574 | 0.7960 | 0.7811 | 0.7596 | **-0.039** | **-0.024** |

Per-seed eval_01: 0.7312 / 0.6969 / 0.7237 (std ≈ 0.015 — large,
larger than 015's 0.017). 021 lands BELOW 011 (no stratification)
and basically ties 016 (10 bins, below floor).

Predicted cross-14 ∈ [0.785, 0.795]. Actual 0.7574. Way outside —
strong falsification of the "5 bins is plateau" hypothesis.

## Granularity is sharply tuned, not a plateau
The granularity sweep now reads:
- 3 bins: 0.7574 (collapse)
- 5 bins: 0.7960 (champion)
- 10 bins: 0.7596 (collapse)

5 bins isn't the floor of an acceptable range — it's a peak. Both
3 bins and 10 bins lose ≈ 0.04 cross-14 vs 5. The win mechanism
needs BOTH narrow-enough bins (each bin spans homogeneous
composition) AND wide-enough bins (per-bin counts above stability
floor). 5 bins is the unique sweet spot in {3, 5, 10}.

GC bin edges for 021: 0.000 / 0.405 / 0.485 / 0.965. Each bin
spans a huge GC range (bin 0: 0-40.5%, bin 2: 48.5-96.5%). The
within-bin GC variance is too large for stratification to actually
homogenize composition. The model still sees a wide GC mixture
inside each "bin" and the stratification benefit dissolves.

## Theory update — v19 → v20
> Granularity is a sharply-tuned dial, not a plateau. The GC
> stratification benefit requires bins narrow enough to actually
> partition composition (failing at 3 bins) AND counts per bin
> above the stability floor (failing at 10 bins). 5 bins is the
> unique sweet spot in this dataset; both directions lose ~0.04.
>
> Mechanistically: stratification helps because it forces the
> sampler to draw signal-weighted and breadth-weighted exemplars
> from each compositional compartment. If bins are too wide, the
> "compartments" aren't homogeneous and stratification just
> shuffles the same big mixture. If bins are too narrow, per-bin
> counts collapse and the model never sees enough breadth-weighted
> exemplars per compartment to learn the local context.
>
> Practical implications:
> - Don't assume "as long as you stratify, granularity doesn't
>   matter much". Granularity matters as much as the choice to
>   stratify at all.
> - The stability floor is per (axis × bin) — narrow bins cross
>   it from below, wide bins lose the partitioning benefit. Both
>   are bad; the sweet spot is unique.
> - Other stratification axes (CpG, dinuc) may have different
>   sweet-spot bin counts. The "5" isn't transferable; the
>   trade-off shape is.

## Next
- 022: dhs_gc_stratified_breadth_only (mirror of 020). 100%
  numsamples-weighted, GC-stratified at 5 bins, 10K per bin.
  Completes the 011/020/022 ablation triangle and quantifies
  exactly how much the breadth-axis adds under stratification.
- After 022 I'll have spent 22 of 30 experiments. Remaining
  budget: 8 experiments. Plan to use them on (a) other
  sequence-derived axes, (b) adding cross-axis interactions
  (e.g. GC × cCRE-class joint stratification), (c) revisiting
  the conservation/cCRE axes now that I understand the
  multiplicative composition rule.
