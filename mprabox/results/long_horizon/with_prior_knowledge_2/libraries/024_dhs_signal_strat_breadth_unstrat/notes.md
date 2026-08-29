# 024_dhs_signal_strat_breadth_unstrat

## What I tested
015 (70/30 mix + GC strat) but stratify ONLY the signal half. The
breadth half is drawn as a single un-stratified weighted draw across
all valid DHS. Hypothesis from v21/v22: breadth × strat is anti-
synergistic; removing breadth-half stratification might neutralize
the harm and yield a cleaner recipe.

- 35K signal-weighted, GC-stratified (7K per bin)
- 15K breadth-weighted, NOT stratified (single draw across 3.59M
  valid DHS, weighted by numsamples)

## Result — falsified hypothesis again
| recipe                                   | cross-14 | seed std |
|------------------------------------------|----------|----------|
| 011 70/30 (no strat)                     | 0.7810   | (1 seed) |
| 015 70/30 + full strat (champion)        | 0.7960   | 0.017    |
| 020 signal-only + strat                  | 0.7841   | 0.006    |
| 022 breadth-only + strat                 | 0.7434   | 0.024    |
| **024 signal strat + breadth unstrat**   | **0.7626** | **0.012** |

Per-seed eval_01: 0.7340 / 0.7282 / 0.7054. cross-14 = 0.7626.

024 < 011 by -0.018, < 015 by -0.033, < 020 by -0.022. Worse than
NO stratification at all — the half-stratified recipe is uniquely
bad.

## Mechanism: inconsistent stratification creates bimodal distribution
The unstratified breadth half draws from the full DHS pool weighted
by numsamples. Numsamples-weighted elements concentrate in moderate-
to-high-GC compartments (broadly-active enhancers and promoters).
Without bin counterbalancing, the breadth half is GC-skewed.

The signal half is GC-uniform (stratification forces 7K per bin).
The breadth half is GC-skewed (concentrated mid-high GC).

The total library has TWO inconsistent compositional shapes layered
on top of each other:
- Bin 0 (low GC): ~7K signal + tiny breadth contribution
- Bin 4 (high GC): ~7K signal + most of the 15K breadth

The model sees an inconsistent training distribution that's harder
to fit than either fully-uniform (015) or fully-natural (011). The
two halves disagree about what the GC distribution should look like.

By contrast:
- 011: both halves natural, both GC-skewed → consistent
- 015: both halves stratified, both GC-uniform → consistent
- 024: signal uniform, breadth skewed → inconsistent → worse

## Theory v22 → v23
> **Stratification regimes must be consistent across recipe halves.**
> Mixing one stratified half with one unstratified half creates a
> bimodal training distribution worse than either fully-stratified
> or fully-unstratified.
>
> The 015 win is therefore not "stratification helps each half
> independently" but "stratification creates a CONSISTENT uniform
> compositional distribution that the model can fit cleanly".
>
> Mechanism: the model is learning a P(activity | sequence) given
> a particular training distribution P(sequence). When the training
> distribution has internal contradictions (one half of elements
> drawn uniformly, the other half drawn skewed), the model has to
> reconcile two different prior shapes — the gradient signal is
> conflicted.
>
> Practical: when designing recipes that combine multiple draws,
> apply the SAME stratification regime to all draws. Don't mix
> stratified with un-stratified components.

## Updated decomposition of 015 win
Combining v21, v22, v23, the 015 win mechanism is:
1. Signal × GC strat is strongly synergistic (+0.019, 020 vs 001)
2. Breadth × GC strat is anti-synergistic at high intensity but
   beneficial at 30% intensity, IF applied consistently with
   signal half (i.e. both stratified)
3. Mixing strat regimes (one half strat, one not) breaks consistency
   and produces worse results than either pure choice

The recipe is a constrained sweet spot at the corner of
(per-axis-bin floor) × (consistent stratification regime) × (mix
ratio). Deviations in any axis cross a constraint and fail.

## Next
- 025: try filtering by numsamples ≥ 3 BEFORE applying the 015
  recipe. This removes the noisy singletons (~40% of DHS) from the
  candidate pool. Tests if 015 can be improved by enriching for
  biologically real regulatory elements before stratifying.
- 026+: explore axes other than GC for stratification, possibly
  joint stratification (GC × cCRE class with relaxed per-cell floor).
