# 002 random genomic 200bp windows

50,000 non-N 200bp windows uniformly sampled from hg38 chr1/11/19/22 pooled by length.
Seed 0. 3,328 windows rejected for containing N.

## Result
- mean_r across 14 evals = 0.682 (vs. 0.852 for random uniform — WORSE by 0.17)
- eval_01 = 0.698 (vs. 0.862 for random uniform)
- SK-N-SH crashed: 0.42–0.52 (vs. 0.83–0.86 in exp 001)
- HepG2 modest drop: 0.78–0.85 (vs. 0.85–0.91)
- K562 mixed (0.37 worst on eval_08)
- Time 9s

## Why I expected the opposite
Literature (MDC 2025, DREAM 2024) says native sequences are more sample-efficient
at low N. I'm at 50k = low N. I predicted ≥0.86.

## Why I think this happened
Random genomic windows are dominated by:
- Repeats (~50% LINE/SINE/Alu)
- Introns and intergenic — mostly silent in MPRA
- GC ≈ 41% vs. 50% for random uniform

The trained model sees a narrow MPRA response distribution (most sequences silent),
so it learns to predict a narrow range, then fails to capture variance in real-genome
eval sequences that include active regulatory elements.

**Random uniform's wider k-mer/composition distribution induced wider MPRA
activity → more learnable signal per sequence, even though the sequences are
"unrealistic".**

## Theory update
For S2A model training at 50k scale, **label dynamic range matters more than
sequence naturalness**. A library should drive the assay across its dynamic
range, not sample evenly from the genome (which is mostly inert).

The "broaden activity distribution" lever has two routes:
1. Enrich for known regulatory elements (active end)
2. Add control sequences that span composition broadly (variance route)

Next experiment should test route 1: known regulatory elements (ENCODE cCREs).
