# 018_dhs_70_30_dinuc_entropy_stratified

## What I tested
015's pattern with dinucleotide Shannon entropy as the
stratification axis. Dinuc entropy is a smooth density metric (no
zero-mass, no degenerate denominators), so it should pass the
"smooth distribution" criterion that CpG O/E (017) failed.

## Result — also a clear loss to 015
| metric   | 018    | 015    | 017    | Δ vs 015 |
|----------|--------|--------|--------|----------|
| eval_01  | 0.7141 | 0.7509 | 0.7212 | -0.037   |
| eval_07  | 0.7439 | 0.7986 | 0.7542 | -0.055   |
| eval_08  | 0.6664 | 0.7270 | 0.6719 | -0.061   |
| eval_13  | 0.7327 | 0.7897 | 0.7451 | -0.057   |
| cross-14 | 0.7548 | 0.7960 | 0.7611 | -0.041   |

Per-seed eval_01: 0.7314 / 0.7276 / 0.6834 (std ≈ 0.022).

018 even loses to 011 baseline (0.7811 cross-14).

## Why dinuc entropy failed
Dinuc entropy distribution is concentrated in a narrow band
(5%-95% spans only 0.905-0.976). The lowest-entropy bin (entropy <
0.934) captures sequences with biased composition — most often
**repeats and simple-repeat regions** (satellite repeats,
microsatellites, low-complexity sequences). Forcing 7K signal-
weighted draws from this bin pulled in:
- Repeat elements that happen to be DHS but don't carry
  cell-type-portable regulatory grammar.
- Composition-skewed sequences that look like noise to a
  generalization-focused model.

Likewise, the highest-entropy bin (entropy > 0.967) over-samples
the most-uniform sequences — also unusual, but in the opposite
direction.

## Theory update — v16 → v17
> **Stratification helps only when EVERY bin contains useful
> regulatory examples.** GC stratification works because GC-poor
> DHS are still real regulatory elements (just from a different
> chromatin compartment). CpG O/E and dinuc entropy stratification
> fail because their tail bins concentrate repeat / low-complexity
> sequences that don't carry transferable regulatory grammar.
>
> The lever is **structured diversity** — diversity along an axis
> where every bin contains rich regulatory content — not diversity
> per se. Mechanistically, GC content is causally upstream of
> regulatory class (promoter vs enhancer) so GC-bins partition the
> regulatory landscape; CpG O/E and entropy partition the genomic
> compartment landscape, which includes non-regulatory regions.
>
> Practical rule for axis design: prefer axes that vary across
> CHROMATIN STATE rather than across SEQUENCE STATISTICS. GC
> happens to satisfy both because it tracks isochore boundaries
> which track regulatory landscape.

## Across 4 sequence-axis tests
| exp | axis | bins | result | reason |
|-----|------|------|--------|--------|
| 015 | GC content | 5 | **WIN** | every bin = real regulatory |
| 016 | GC content | 10 | LOSS | per-cell stability floor |
| 017 | CpG O/E | 5 | LOSS | degenerate distribution |
| 018 | dinuc entropy | 5 | LOSS | tail bins = repeats |

GC is uniquely good among single-number sequence axes.

## Next
Pivot from "find another sequence axis" to "stack GC with another
lever". Best candidate: combine GC stratification (015) with cCRE-
overlap filter (008). Both tied/won vs baseline; combining tests
whether their orthogonal mechanisms add.

If 019 lifts further, the recipe is GC × cCRE filter. If 019 ties
015, the cCRE filter is dominated by GC stratification (as 014/017
were). If 019 loses, the cCRE filter is incompatible with GC
stratification due to subset-shifted distributions.
