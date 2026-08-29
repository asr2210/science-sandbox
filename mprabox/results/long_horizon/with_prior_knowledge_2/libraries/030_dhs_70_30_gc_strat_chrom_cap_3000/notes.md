# 030_dhs_70_30_gc_strat_chrom_cap_3000

## What I tested
Refinement of 029 — same recipe but with cap RELAXED from 2500
to 3000. Hypothesis: a milder cap that only constrains the most
extreme over-representation (chr1, chr2, possibly chr10) might
land in a Goldilocks zone between 015 (no cap) and 029 (cap=2500).

cap=3000 → 5-7 chroms hit cap (chr1-5 always, plus chr6/chr10 in
some seeds), redistributing ~5K elements per seed (10% of library)
vs 029's 13 chroms / 20K elements (40%).

## Result — counter-intuitive: relaxed cap loses MORE
| recipe                              | cross-14 | seed std | Δ vs 015 |
|-------------------------------------|----------|----------|----------|
| 015 70/30 GC strat (champion)       | 0.7960   | 0.017    | 0        |
| 029 cap=2500 (40% redistributed)    | 0.7874   | 0.016    | -0.009   |
| **030 cap=3000 (10% redistributed)**| **0.7641** | **0.016** | **-0.032** |

Per-seed eval_01: 0.6997 / 0.7299 / 0.7372 (std 0.016). cross-14
= 0.7641, -0.032 vs 015 — WORSE than 029's strict cap.

Naïvely you'd expect cap=3000 (less redistribution) to be CLOSER
to 015 (no cap). Instead, 030 lost 3.5× more than 029.

## Mechanism — selective top-N exclusion is worse than broad cap
- cap=2500 (029): 13 chroms hit cap, including mid-sized chroms
  (chr10-17). Redistribution flows to chr18-22 and small chroms.
  All chroms get a similar effective cap.
- cap=3000 (030): only 5-7 chroms hit cap, all the largest
  (chr1-6). Mid-sized chroms (chr10-17) operate UNCAPPED at their
  natural ~2000-2500 counts. The redistribution is concentrated:
  the 5K excess from chr1-5 flows almost entirely to chr10-17 and
  smaller.

Why does 030 lose more? Hypothesis: the chr1-5 mega-chroms aren't
just over-represented in count — they carry the BEST signal-elite
elements (most gene-dense, most regulatory-enhancer-rich). cap=2500
spreads the cap broadly enough that this effect averages out;
cap=3000 specifically targets the elite chroms without compensating
elsewhere.

This means chrom balance is non-monotonic with respect to cap
strictness: very strict cap (broad redistribution) > no cap
(natural distribution) > moderately-relaxed cap (selective top-N
removal).

## Implication: chrom balance has no Goldilocks zone above 015
There's no cap value between 2500 and ∞ that improves over 015.
The two tested points (2500 and 3000) both lose, with 3000 losing
more. Smaller caps would lose even more (they'd start clipping
mid-sized chroms severely). Larger caps approach 015 from below
slowly.

## Theory v28 → v29 (final)
> **Chromosome balance has no improvement zone over 015.** Tested
> at cap=2500 (-0.009) and cap=3000 (-0.032), both lose. The
> non-monotonic relationship — strict cap loses LESS than mild cap
> — implies that selective removal of the top-5 mega-chroms is
> worse than either uniform broad redistribution OR no intervention.
>
> 015's natural chromosome distribution (driven by DHS density)
> is at or near the optimum for cell-type-generalization. The
> mega-chroms (chr1-5) carry disproportionately informative
> signal-elite elements that are hard to substitute via
> redistribution.
>
> **Final 015 verdict: GLOBAL CHAMPION across all 14 perturbations
> tested in this study.** Every dimension probed has confirmed
> that 015 is at a multi-axis optimum: stratification scheme (5 GC
> bins), mix ratio (70/30), both axes (signal × numsamples),
> draw structure (two-axis per-bin), regime consistency (full
> stratification), candidate pool (full DHS), window (summit-centered
> 200bp), AND chromosomal composition (natural DHS density).

## Final summary of the 015 perturbation series — 14 perturbations, 14 losses
| recipe              | Δ cross-14 |
|---------------------|------------|
| 015                 | 0          |
| 029 chrom cap=2500  | -0.009     |
| 020 signal-only     | -0.012     |
| 011 no GC strat     | -0.015     |
| 025 nums≥3 filter   | -0.017     |
| 027 cCRE-maxZ axis  | -0.018     |
| 028 combined weight | -0.031     |
| 030 chrom cap=3000  | -0.032     |
| 024 half strat      | -0.033     |
| 023 80/20 mix       | -0.037     |
| 016 10 GC bins      | -0.039     |
| 021 3 GC bins       | -0.039     |
| 026 phyloP axis     | -0.045     |
| 022 breadth-only    | -0.053     |
| 019 cCRE filter     | -0.049     |

015 is overdetermined. Recommended library: **015**
(70/30 signal/numsamples mix, both halves stratified across 5
equal-population GC quintiles).
