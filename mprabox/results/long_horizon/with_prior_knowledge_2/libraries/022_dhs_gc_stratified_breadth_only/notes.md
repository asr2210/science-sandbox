# 022_dhs_gc_stratified_breadth_only

## What I tested
Mirror ablation of 020. Same GC stratification (5 equal-pop bins),
but with 100% numsamples (breadth) weighting and no signal axis.
10K breadth-weighted draws per bin = 50K total.

Together with 011 (no strat, 70/30 mix), 020 (strat + signal-only),
and 022 (strat + breadth-only), this completes the decomposition
that isolates how each biology axis interacts with stratification.

## Result — surprising asymmetry, big collapse
| recipe                          | cross-14 | eval_01 | seed std |
|---------------------------------|----------|---------|----------|
| 001 signal only                 | 0.7653   | 0.7242  | (1 seed) |
| 002 breadth only                | 0.7534   | 0.7152  | (1 seed) |
| 011 70/30 mix                   | 0.7810   | 0.7383  | (1 seed) |
| 015 70/30 + GC strat (champion) | 0.7960   | 0.7509  | 0.017    |
| 020 signal + GC strat           | 0.7841   | 0.7401  | 0.006    |
| **022 breadth + GC strat**      | **0.7434** | **0.7041** | **0.024** |

Per-seed eval_01: 0.6701 / 0.7163 / 0.7258 (range 0.056 — biggest
seed instability of the entire series).

Predicted cross-14 ∈ [0.770, 0.790]. Actual 0.7434. Way below — even
worse than 002 (pure breadth, no stratification). **GC stratification
applied to breadth-only weighting actively HARMS the result.**

## Asymmetric interaction with stratification
| axis                | no strat | + GC strat | Δ      |
|---------------------|----------|------------|--------|
| signal (001 → 020)  | 0.7653   | 0.7841     | +0.019 |
| breadth (002 → 022) | 0.7534   | 0.7434     | -0.010 |
| 70/30 (011 → 015)   | 0.7810   | 0.7960     | +0.015 |

**Stratification's interaction is axis-dependent**, not axis-agnostic.
It HELPS signal-weighted draws and HURTS breadth-weighted draws.
This was completely invisible from 015/020 alone — needed 022 to
isolate.

## Mechanism hypothesis
Breadth-axis (numsamples) elements concentrate biologically in
moderate-GC compartments — promoters and broadly-active elements
have natural GC bias toward CpG-island-overlapping regions. Within
extreme-GC bins (very low or very high), there are FEW
high-numsamples elements; the breadth-weighted draw exhausts the
top-numsamples tail quickly and is forced into low-numsamples
elements with unusual composition. These are the worst training
examples: weak biological signal plus extreme composition.

Signal axis doesn't have this problem: high-mean_signal elements
exist throughout the GC range. Stratifying ensures the model sees
intense regulatory elements across all compositions — uniformly
informative.

The 015 win mechanism is therefore not "breadth axis adds diversity
under stratification". It's: **signal axis × stratification is the
real win; the 30% breadth allocation is a small enough perturbation
that the harm doesn't dominate**, and may even add small benefit by
providing a different selection criterion within each bin (which
breaks signal-weight near-duplicates across seeds).

## Decomposition update
The 015 lift over 011 (+0.015) decomposes as:
- Signal axis × strat alone (020 vs 001): +0.019
- Removing 100% breadth from strat (020 vs 022): +0.041
- Adding 30% breadth back into strat (015 vs 020): +0.012

The +0.012 gain from re-adding 30% breadth to a signal+strat base is
real, but it's a SMALL perturbation around a recipe that's already
strong. The breadth axis at 100% intensity destroys the recipe by
~0.04. Mix ratio matters precisely because the breadth axis under
stratification is fragile.

## Per-seed instability tells the story
- 020 (signal + strat): per-seed std 0.006
- 022 (breadth + strat): per-seed std 0.024 (4× higher)
- 015 (mix + strat): per-seed std 0.017 (intermediate)

The breadth-axis under stratification is not just less effective —
it's UNSTABLE across seeds. The within-bin candidate pool of
high-numsamples elements is small in extreme-GC bins; different
seeds pick different fillers, leading to wildly different results.

## Theory v20 → v21
> **Stratification's interaction with biology axes is asymmetric, not
> uniform.** GC stratification × signal-axis is strongly synergistic
> (+0.019). GC stratification × breadth-axis is anti-synergistic
> (-0.010). The 015 win is primarily "signal × strat", with the
> 70/30 mix providing a small additional lift only because at 30%
> intensity the breadth axis's harm doesn't dominate.
>
> Mechanism: breadth-weighted elements are biologically concentrated
> in moderate-GC compartments. Forcing draws across all GC bins
> exhausts the top-broadness tail in extreme bins and pulls in
> noisy fillers. Signal-weighted elements span the full GC range,
> so stratification just selects diverse exemplars per bin.
>
> Practical: when designing recipes, ALWAYS test (axis × stratification)
> in isolation, not just (axis + stratification + mix). The mix can
> mask asymmetric interactions. Interaction direction may invert
> when the axis is changed (e.g. conservation, cCRE class).

## Next
- 023: bracket 70/30 mix ratio under GC stratification. Try 80/20
  (less breadth) — if breadth is fragile under strat, less of it
  may help further. If 80/20 + strat > 015, the optimal mix ratio
  is shifted toward signal under stratification.
- 024+: explore whether other axes (conservation, cCRE) show similar
  asymmetric interactions with stratification, or whether GC × axis
  interactions are uniformly axis-dependent.
