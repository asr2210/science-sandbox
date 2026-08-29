# 025_dhs_70_30_gc_strat_numsamples_filtered

## What I tested
015 with candidate pool restricted to numsamples ≥ 3. This drops
1.66M (46%) of DHS — the singletons (1.23M, observed in only 1 of
733 biosamples) and doubletons (0.43M). Hypothesis: singletons may
be noise / cell-type-specific artifacts that dilute the recipe;
filtering them should enrich the pool for biologically-real
regulatory elements.

Bin edges shifted slightly (0.005/0.385/0.430/0.475/0.535/0.965 vs
015's 0.000/0.375/0.420/0.465/0.525/0.965) — filter biases pool
slightly toward higher GC, as expected (broadly-active elements
overlap CpG islands).

Per-bin candidate pool: 380K-410K (vs 015's 685K-781K). Still
50× larger than per-bin draw count; no risk of pool exhaustion.

## Result — falsified, mild loss
| recipe                                    | cross-14 | seed std |
|-------------------------------------------|----------|----------|
| 015 70/30 + GC strat (champion)           | 0.7960   | 0.017    |
| **025 015 + numsamples >= 3 filter**      | **0.7792** | **0.016** |
| 011 70/30 (no strat)                      | 0.7810   | (1 seed) |
| 019 015 + cCRE-overlap filter             | 0.7472   | 0.040    |

Per-seed eval_01: 0.7592 / 0.7271 / 0.7231 (range 0.036). cross-14
= 0.7792, -0.017 vs 015. Even slightly below 011 (no strat at all).

## Singletons carry useful diversity
The cleanest interpretation: cell-type-specific (singleton) DHS
provide unique training value beyond their numerosity. They likely
include rare regulatory elements with distinctive sequence
features that the model needs to learn to generalize beyond the
labeled cell types. Filtering them out — even at "low-confidence"
threshold — costs ~0.017 cross-14.

This is the OPPOSITE of what a quality-control mindset would
predict. The model isn't bottlenecked by noisy elements; it's
helped by the long tail of cell-type-specific elements.

## Ranking the filter experiments
| filter                                    | cross-14 | Δ vs 015 |
|-------------------------------------------|----------|----------|
| none (015 baseline)                       | 0.7960   | 0        |
| 025 numsamples ≥ 3                        | 0.7792   | -0.017   |
| 019 cCRE-overlap                          | 0.7472   | -0.049   |

cCRE filter is much more harmful than numsamples filter. Both
filters share a mechanism: they bias the candidate pool toward
"canonical regulatory elements" and lose the long tail of
cell-type-specific or non-canonical elements. The cCRE filter is
worse because it also concentrates GC distribution and breaks
per-bin uniformity.

## Theory v23 → v24
> **Cell-type-specific (singleton) DHS contribute training value
> proportional to MORE than their fraction.** Filtering them out
> at numsamples ≥ 3 drops 46% of elements but costs 0.017 cross-14
> — far more than would be expected from candidate-pool diversity
> alone.
>
> Mechanism hypothesis: singletons cover regulatory grammar that
> broadly-active elements don't. The model trained without them
> overfits to "canonical" regulatory elements and generalizes
> worse to held-out cell types where the relevant grammar may be
> dominated by lineage-specific elements.
>
> Practical: do not filter the candidate pool by quality metrics
> like numsamples or cCRE-overlap. The full DHS Index, including
> singletons, is the right candidate pool for diversity.
>
> Combined with v22 (per-axis-bin floor): the 015 recipe selects
> 50K of 3.5M elements via stratified weighted draws. The CHOICE
> of which 50K matters; the SELECTION POOL also matters. Both
> levers cost performance when changed.

## Combined picture of 015 win mechanism (v17-v24)
1. **GC stratification** partitions sequence-composition space into
   5 bins so each compositional regime gets equal training weight.
2. **70/30 mix** within each bin combines signal-axis (intense
   regulatory elements) with breadth-axis (broadly-active elements).
   The breadth axis at 30% intensity adds a small lift but is
   anti-synergistic at 100% (022).
3. **Per-axis-bin floor (3K)** is a hard constraint — both 70/30
   ratio and 5-bin granularity are at the corner of this constraint
   (3K breadth/bin is at the floor).
4. **Consistent stratification regime** — both halves stratified
   together (015) wins; mixing (024) loses.
5. **Full candidate pool** — including singletons. Filtering hurts
   (019, 025).
6. **Single window definition** — summit-centered 200bp. Multi-
   window (009) didn't help.

The 015 recipe is overdetermined: many design choices align at the
sweet spot, with each one verified by ablation as load-bearing.

## Next
- 026: replace breadth axis with conservation axis (phyloP). Test
  if a different second biology axis under consistent stratification
  matches breadth's contribution. 70/30 mix becomes
  (signal × phyloP), both GC-stratified at 5 bins.
- 027+: explore truly orthogonal axes (chromosome stratification,
  TF-density), or sample-definition variants (window shift).
