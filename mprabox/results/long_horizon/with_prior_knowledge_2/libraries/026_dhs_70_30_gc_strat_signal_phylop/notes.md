# 026_dhs_70_30_gc_strat_signal_phylop

## What I tested
015's recipe with the breadth (numsamples) axis REPLACED by phyloP
conservation. Both axes consistently GC-stratified. Tests whether
015's lift comes from numsamples specifically or from "any second
biology axis under consistent stratification".

- 35K mean_signal-weighted, GC-stratified (7K/bin)
- 15K phyloP-weighted (max(0.01, score) flooring), GC-stratified (3K/bin)

## Result — substantial loss, axes are NOT interchangeable
| recipe                                | cross-14 | seed std | Δ vs 015 |
|---------------------------------------|----------|----------|----------|
| 015 signal × numsamples + GC strat    | 0.7960   | 0.017    | 0        |
| 020 signal-only + GC strat            | 0.7841   | 0.006    | -0.012   |
| **026 signal × phyloP + GC strat**    | **0.7510** | **0.017** | **-0.045** |
| 007 phyloP alone                      | 0.7367   | (1 seed) | -0.059   |

Per-seed eval_01: 0.7337 / 0.6971 / 0.7005. cross-14 = 0.7510, ALSO
worse than 020 by -0.033 — adding phyloP as 30% mix is ACTIVELY
harmful relative to dropping the second axis entirely.

## The second axis must be biologically aligned to regulatory activity
The 015 win is not "any orthogonal biology axis under strat". Numsamples
is uniquely the right second axis because it directly proxies what we
want the model to generalize to: regulatory activity across cell types.

Conservation (phyloP) is "orthogonal" to signal but biologically
mismatched. Highly conserved sequences include:
- Conserved exonic regions (NOT regulatory)
- Long-range conserved enhancers in inactive cell-type contexts
- Untranslated regions
- Highly constrained but non-DHS-active sequences

Forcing the model to learn from phyloP-weighted DHS pulls in
biologically conserved-but-functionally-inactive elements that
confuse the activity prediction task.

This explains why 026 < 020: dropping the second axis loses some
diversity, but adding the wrong axis adds BAD information that
actively hurts.

## Theory v24 → v25
> **The second axis in the 015 mix must be biologically aligned to
> the prediction target (regulatory activity), not just orthogonal
> to the first axis.** Numsamples works because it directly indexes
> "broadness of regulatory activity across cell types" — exactly
> what generalization beyond labeled cell types requires. PhyloP
> doesn't because conservation is orthogonal to regulatory activity
> in the assayed cell types.
>
> Mechanism: at 30% intensity under consistent stratification, the
> second axis selects ~3K elements per GC bin that the signal axis
> would miss. If those elements are biologically informative
> (numsamples → broadly active enhancers/promoters), they enrich
> training. If they're biologically misaligned (phyloP → conserved
> but inactive elements), they pollute training.
>
> This refines v23 (consistency principle): consistency of the
> stratification regime is necessary, but the second axis itself
> must be the right kind of biology.
>
> Practical: candidates for substitute axes need biological
> alignment. cCRE-maxZ (continuous chromatin Z-score across cell
> types) is closer to numsamples than phyloP and might work.
> Anything based on conservation, motif content, or sequence
> intrinsics is likely to fail.

## Updated ranking of axis substitutes for 015's breadth half
| axis (under signal + GC strat)    | cross-14 | aligned? |
|------------------------------------|----------|----------|
| numsamples (015)                   | 0.7960   | yes      |
| nothing (020 signal only)          | 0.7841   | n/a      |
| phyloP conservation (026)          | 0.7510   | no       |

Nothing substitutes for numsamples among biology axes I've tried.

## Next
- 027: try cCRE-maxZ as the second axis under consistent strat.
  cCRE-maxZ is closer to "regulatory activity broadness" than
  phyloP. If 027 ≈ 015, axis-alignment is the key. If 027 < 015,
  numsamples is uniquely the right metric and chromatin-Z proxies
  don't substitute.
