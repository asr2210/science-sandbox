# Experiment 007 — All-chromosome random genomic

## Design
50,000 windows allocated proportionally to chromosome length across
chr1-22, chrX, chrY. ~4k from chr1 down to ~750 from chr21/chrY.

## Results vs 5-chromosome multi-chrom (004)
| eval | multi-chrom (004) | all-chrom (007) | Δ |
|------|-------------------|-----------------|---|
| 01 ★ | **0.5553** | 0.5086 | -0.05 |
| 03 | 0.5603 | 0.5239 | -0.04 |
| 04 | 0.5086 | 0.3968 | -0.11 |
| 06 | 0.5552 | 0.5097 | -0.05 |
| 07 | 0.6284 | 0.6375 | +0.01 |
| 08 | 0.0208 | **-0.1242** | -0.15 |
| 10 | 0.5008 | 0.4592 | -0.04 |
| 13 | 0.6135 | 0.6222 | +0.01 |

**Surprising negative result: more is less.** All-chromosome diversity
underperforms a 5-chromosome subset on the primary metric (-0.05).

## Why? GC content shifted lower
- chr8/19/21/22/X subset: GC ≈ 43% (chr19 alone GC ≈ 48%)
- All chromosomes: GC ≈ 41% (whole-genome average)

In exp 004, chr19's over-representation (10k/50k = 20% of library) raised
the GC distribution toward what eval_01/02/03/06 prefer. Proportional
sampling halved chr19's representation (949/50,000 = 1.9%) and the
resulting GC drop hurt scores.

eval_08 going *negative* (-0.124) is the strongest signal — eval_08
clearly has a high-GC target distribution; the all-chrom library
mismatches it harder than chr19-only or even chr8-rich subsets.

## Theory v6 confirmed and refined
The library should optimize compositional match, not just diversity.
"Diversity" was a heuristic that happened to align with composition in
multi-chrom-5 because chr19 (GC-rich) was over-represented. Genome-wide
proportional sampling sacrifices that compositional alignment.

## What this tells me
- More natural diversity does NOT monotonically help.
- The compositional distribution of the library matters at least as
  much as the sample count or chromosome count.
- Need to think about *compositional engineering*: what's the optimal
  GC / k-mer distribution to use for training?

## Next ideas
1. **GC-targeted sampling**: sample to match a chosen GC distribution.
2. **Multi-chrom GC-rich subset**: e.g., all chromosomes but resample
   regions to enrich for GC=45-55%.
3. **Stratified sampling**: cover the GC range uniformly.
