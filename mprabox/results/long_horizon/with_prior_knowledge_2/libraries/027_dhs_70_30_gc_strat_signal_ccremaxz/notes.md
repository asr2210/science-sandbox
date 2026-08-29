# 027_dhs_70_30_gc_strat_signal_ccremaxz

## What I tested
015's recipe with the breadth (numsamples) axis REPLACED by
cCRE-maxZ — continuous chromatin Z-score across cell types.
cCRE-maxZ is biologically closer to numsamples than phyloP both
proxy "regulatory broadness" but with different geometries:
- numsamples = COUNT of biosamples where DHS is observed (1-365)
- cCRE-maxZ = MAX z-score of chromatin signals across cell types

Tests whether ANY broadness-aligned axis substitutes for
numsamples or only numsamples specifically.

- 35K mean_signal-weighted, GC-stratified (7K/bin)
- 15K cCRE-maxZ-weighted (max(0.01, score) flooring), GC-stratified
  (3K/bin)

## Result — partial substitution but still loses
| recipe                                    | cross-14 | seed std | Δ vs 015 |
|-------------------------------------------|----------|----------|----------|
| 015 signal × numsamples + GC strat        | 0.7960   | 0.017    | 0        |
| 020 signal-only + GC strat                | 0.7841   | 0.006    | -0.012   |
| **027 signal × cCRE-maxZ + GC strat**     | **0.7783** | **0.010** | **-0.018** |
| 026 signal × phyloP + GC strat            | 0.7510   | 0.017    | -0.045   |
| 022 numsamples-only + GC strat            | 0.7434   | 0.024    | -0.053   |

Per-seed eval_01: 0.7434 / 0.7219 / 0.7421 (range 0.022). cross-14
= 0.7783 — better than phyloP substitution (-0.018 vs -0.045) but
still worse than 015 (-0.018) and worse than just dropping the
second axis (020 = 0.7841, +0.006 over 027).

## Numsamples is uniquely informative for cell-type generalization
Ranking of axis substitutes:
1. numsamples (015): 0.7960 — uniquely best
2. nothing (020): 0.7841 — second axis isn't necessary
3. cCRE-maxZ (027): 0.7783 — slightly worse than nothing
4. phyloP (026): 0.7510 — much worse than nothing

The two close-in-biology candidates (numsamples and cCRE-maxZ)
should be highly correlated — both measure "regulatory activity
breadth across cell types". Yet numsamples wins by 0.018. Why?

Hypothesis 1: COUNT vs INTENSITY semantics
- numsamples: discrete COUNT of biosamples with this DHS active.
  Selects DHS active in MANY contexts.
- cCRE-maxZ: continuous MAX intensity across cell types. Selects
  DHS with one VERY STRONG context.
A DHS with numsamples=200 is broadly active. A DHS with
cCRE-maxZ=8 may be a cell-type-specific super-enhancer (high
intensity in one tissue, near-zero elsewhere).

For a model that must generalize beyond labeled cell types, the
"broadly active in many contexts" elements are more informative —
they encode regulatory grammar that transfers across cell types.
"Strong in one context" elements may encode lineage-specific
super-enhancer grammar that doesn't transfer.

Hypothesis 2: cCRE-overlap bias
cCRE-maxZ is non-zero only for cCRE-overlapping DHS (38%). The
breadth-axis draw concentrates on cCRE-DHS, partially reproducing
the 019 cCRE-overlap filter problem (cost: -0.049). 027 is milder
(-0.018) because the signal half still uses full pool, so non-cCRE
DHS contribute via signal-axis selection.

Both hypotheses likely contribute.

## Theory v25 → v26
> **Cross-cell-type COUNT (numsamples) is uniquely informative for
> the second axis of 015**, even compared to closely-related
> continuous chromatin-intensity proxies. The lesson: for a
> sequence-to-activity model meant to generalize beyond labeled
> cell types, the second axis should encode HOW MANY contexts an
> element is active in, not HOW INTENSE it is in any single context.
>
> Mechanism: cell-type-specific super-enhancers (high cCRE-maxZ)
> encode lineage-specific grammar that doesn't transfer. Broadly-
> active elements (high numsamples) encode foundational regulatory
> grammar that transfers. The model needs the latter to predict
> activity in held-out cell types.
>
> Practical: numsamples is irreplaceable as the second axis. Future
> recipes should retain numsamples and explore additions (third
> axis, sample-definition variants, chromosome balance) rather
> than substitutions of either axis.

## Closing the substitution-experiment series
We've now tested:
- 020: drop second axis → -0.012
- 022: keep only second axis → -0.053
- 023: shift mix ratio → -0.037
- 024: half-stratify → -0.033
- 025: filter pool → -0.017
- 026: substitute axis (phyloP) → -0.045
- 027: substitute axis (cCRE-maxZ) → -0.018

EVERY perturbation of 015 LOSES. The recipe is overdetermined.

## Next
- 028: structural test of recipe — collapse the two-axis per-bin
  draws into a single per-element combined-weight draw.
  Tests if the "two separate weighted draws per bin" structure is
  load-bearing or just an implementation detail of "use a 70/30
  mix under stratification".
