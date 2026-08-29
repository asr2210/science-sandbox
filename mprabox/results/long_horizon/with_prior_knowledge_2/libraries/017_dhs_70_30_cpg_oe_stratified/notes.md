# 017_dhs_70_30_cpg_oe_stratified

## What I tested
015's pattern (locked 70/30, equal-population sequence-axis
stratification) but with CpG O/E (observed/expected CpG
dinucleotides) instead of GC content. Tests whether the 015 win
generalizes to any sequence-composition axis or whether GC is
special.

## Result — clear loss to 015
| metric   | 017    | 015 (champ) | 011    | Δ vs 015 |
|----------|--------|-------------|--------|----------|
| eval_01  | 0.7212 | 0.7509      | 0.7383 | -0.030   |
| eval_07  | 0.7542 | 0.7986      | 0.7751 | -0.044   |
| eval_08  | 0.6719 | 0.7270      | 0.7041 | -0.055   |
| eval_13  | 0.7451 | 0.7897      | 0.7644 | -0.045   |
| cross-14 | 0.7611 | 0.7960      | 0.7811 | -0.035   |

Per-seed eval_01: 0.7322 / 0.7342 / 0.6971 (std ≈ 0.021 — similar
to 016's instability, also has a seed=2 outlier).

017 even loses to 011 (no stratification at all).

## Why CpG O/E failed
The CpG O/E distribution is heavily degenerate:
- 5th percentile = 0.000 (5% of DHS have zero CpG dinucleotides)
- 25th percentile = 0.088
- Top of distribution: 40+ (artifacts of low-denominator sequences
  with rare C/G but happens-to-have CpG)

Equal-population quintile binning over this distribution produced:
- bin 0: zero-CpG sequences (746K elements, but composition-
  homogeneous)
- bin 4: 0.358-40+ range (includes degenerate high-O/E artifacts)

The library ended up forcing 7K from the zero-CpG-desert bin and
7K from the artifact-prone high-O/E bin — both compositional
extremes that don't transfer well to the held-out evals.

## Theory update — v15 → v16
> **Sequence-derived axes are NOT all equivalent.** The 015 win is
> not just "any sequence axis lifts" — the axis must have:
> 1. Smooth, non-degenerate distribution across its full range.
> 2. Biological meaning at every quantile (not just at the median).
> 3. No edge-case artifacts in the binning scheme.
>
> GC content satisfies all three: every sequence has a well-defined
> GC value, distribution is approximately continuous, no
> degeneracies. CpG O/E fails (1) and (3): heavy zero-mass at the
> bottom, denominator-driven artifacts at the top.
>
> This narrows the axis-design search: future sequence-derived
> axes should be metrics that vary smoothly across all DHS, not
> ratio-based metrics with degenerate denominators.

## Comparison vs 014/015 — three failure modes
- 014 (cCRE class balance): orthogonal lever, stable basin (std
  0.001), but trade-vector wrong direction on cross-14.
- 016 (GC 10 bins): right axis, wrong granularity — crossed
  per-(axis × bin) stability floor.
- 017 (CpG O/E 5 bins): right granularity, wrong axis — degenerate
  distribution forced compositional extremes.

015's win comes from a specific combination: GC + 5 bins + 70/30
locked ratio. Each parameter matters.

## Next
- 018: try a sequence-derived axis with smooth distribution. Best
  candidate: dinucleotide Shannon entropy (16-dim entropy across
  all dinucleotides), which has no degeneracies and varies
  continuously. If it lifts like GC, the mechanism is "smooth
  sequence-composition stratification". If it doesn't, GC is
  uniquely good for some content-specific reason.
- Alternative direction: test whether 015's GC stratification
  STACKS with 014's cCRE class structure (despite 014's wrong
  trade-vector, the components might combine). Per-(axis × bin)
  budget needs care: 5 GC bins × 3 cCRE classes = 15 cells, 35K/15
  = 2.3K signal per cell — below floor. So this stack would need
  fewer GC bins (e.g., 3 GC × 3 class = 9 cells, ~3.9K per cell).
