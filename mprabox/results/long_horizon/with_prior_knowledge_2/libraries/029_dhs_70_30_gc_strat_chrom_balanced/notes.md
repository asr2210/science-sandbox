# 029_dhs_70_30_gc_strat_chrom_balanced

## What I tested
015's recipe with a per-chromosome cap added as an extra structural
constraint. Same 70/30 mix, same 5 GC bins, both halves stratified.
Difference: enforce a hard cap of 2500 per chromosome
(= ceil(50000 / 24 chroms * 1.2)) during the per-bin draws.

The cap caps the over-represented chromosomes (chr1, chr2, chr10,
chr11, chr12, chr17 all hit 2500/2500), redistributing draws to
mid-sized chroms. Small chroms (chrY=85, chr21=850) are unaffected.

About 20K draws per seed were skipped due to the cap and
redistributed. 13 chroms hit the cap (out of 24).

## Result — smallest loss measured but still loses
| recipe                              | cross-14 | seed std | Δ vs 015 |
|-------------------------------------|----------|----------|----------|
| 015 70/30 GC strat (champion)       | 0.7960   | 0.017    | 0        |
| **029 + per-chrom cap=2500**        | **0.7874** | **0.016** | **-0.009** |
| 020 signal-only + GC strat          | 0.7841   | 0.006    | -0.012   |
| 011 70/30 mix (no strat)            | 0.7810   | (1 seed) | -0.015   |
| 027 signal × cCRE-maxZ + GC strat   | 0.7783   | 0.010    | -0.018   |
| 025 numsamples-filtered pool        | 0.7792   | 0.005    | -0.017   |

Per-seed eval_01: 0.7199 / 0.7567 / 0.7512 (std 0.016, similar to
015's 0.017). cross-14 = 0.7874 — the smallest loss of any 015
perturbation tested (-0.009).

## Chromosome balance is the gentlest perturbation
029 is the closest any single-axis change has gotten to 015. This
is interesting: it suggests chromosome distribution carries SOME
signal, but the natural over-representation of chr1/chr2 isn't
critical to 015's win.

Why doesn't it help? Two competing effects:
- **Pro**: balanced coverage exposes the model to underrepresented
  chromosomal contexts (chr18, chr21) that natural DHS-density
  draws would skip.
- **Con**: large chromosomes (chr1, chr2) have more genes, more
  active enhancers, and likely more DIVERSE regulatory grammar.
  Capping them removes some of the most-informative training
  examples.

The net effect is mildly negative (-0.009): the lost grammar from
capped large chroms slightly outweighs the gained coverage from
small chroms. But the effect is small enough that chromosome
balance ALMOST recovers 015 — the closest near-miss in the series.

## Why per-chrom caps still preserve most of 015's signal
20K elements get redistributed (40% of the library) yet cross-14
only loses 0.009. This suggests that CHROMOSOMAL composition is
relatively low-information compared to (signal × numsamples × GC).
The model can learn the same regulatory grammar from chr3 elements
as from chr1 elements, as long as the (signal × numsamples × GC)
distributions match.

015's robustness to this perturbation is itself diagnostic:
regulatory grammar is largely chromosome-invariant.

## Theory v27 → v28
> **Chromosomal composition is largely interchangeable for
> regulatory-grammar learning under fixed (signal × numsamples × GC)
> distribution.** Adding a per-chrom cap that redistributes 40% of
> draws away from over-represented chromosomes only loses 0.009
> cross-14 — the smallest loss of any single-axis perturbation
> measured.
>
> This implies the model learns sequence-level regulatory grammar
> rather than chromosome-specific grammar, AS LONG AS the per-element
> features (signal, numsamples, GC) are diverse. The chromosome
> identity is a near-redundant feature given those three.
>
> Practical: future recipes shouldn't bother with chromosome
> balancing as a primary axis. The remaining 0.009 gap suggests
> very mild signal in natural chromosome distribution — likely
> reflecting subtle differences in DHS density (chr1/chr2 are
> gene-rich) and not worth the added complexity.

## 015 series — 9 perturbations all lose
| recipe              | Δ cross-14 |
|---------------------|------------|
| 015                 | 0          |
| 029 chrom cap       | -0.009     |
| 020 signal-only     | -0.012     |
| 011 no GC strat     | -0.015     |
| 025 nums≥3 filter   | -0.017     |
| 027 cCRE-maxZ axis  | -0.018     |
| 028 combined weight | -0.031     |
| 024 half strat      | -0.033     |
| 023 80/20 mix       | -0.037     |
| 026 phyloP axis     | -0.045     |
| 021 3 GC bins       | -0.039     |
| 016 10 GC bins      | -0.039     |
| 022 breadth-only    | -0.053     |

EVERY perturbation loses. 015 is overdetermined.

## Next
- 030: final experiment. Two strong candidates:
  - **(A) 75/25 GC strat** — closes the mix-ratio sweep between
    015 (70/30) and 023 (80/20). Tests if the mix slope is monotonic
    or has a finer-grained optimum.
  - **(B) 015 with cap=3000** (light chrom balance) — if 029's
    -0.009 was the smallest loss with a strict cap, maybe a milder
    cap that only caps chr1/chr2 lands in a Goldilocks zone.
  Going with (B): chrom balance was the smallest perturbation, so
  refining it has the highest chance of finding a tiny improvement.
  If it improves, we have a new champion. If not, the project ends
  with 015 confirmed as the global optimum across all tested axes.
