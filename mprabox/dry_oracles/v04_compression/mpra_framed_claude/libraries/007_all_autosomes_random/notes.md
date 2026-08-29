# 007_all_autosomes_random

50k random 200bp windows from all 22 GRCh38 autosomes, weighted by
length. Same procedure as 002 except more chromosomes.

## Result
eval_01: 0.4898 (vs 002: 0.4967, -0.007)
mean across 14 evals: 0.515 (vs 002: 0.524)

## Per-eval delta vs 002 (6 chroms)
- eval_01: -0.007
- eval_03: -0.009
- eval_04: -0.015
- eval_06: -0.008
- eval_07: -0.002
- eval_08: -0.007
- eval_10: -0.014
- eval_13: -0.008

All slightly worse. Tiny but consistent.

## Interpretation
Broader autosome coverage SLIGHTLY HURTS. Hypothesis: the 6
chromosomes used in 002 (1, 11, 19, 20, 21, 22) happen to be more
gene-dense than the genome average (chr19 and chr22 are among the
top in gene density). The 22-autosome sample is more diluted with
gene-poor, repeat-heavy chromosomes (e.g., chr Y not included but
chrs 1-18 contain large centromeric and repetitive regions).

So: the natural-data plateau is real, and within "natural" there's a
small bonus from gene-richness. The 0.50 ceiling is *almost*
fundamental for our 50k×200bp natural-sequence budget — but a
~0.005-0.015 lift may be available from biasing toward gene-rich
regions.

## Implication for next experiment
Test transcribed/gene-proximal sampling explicitly. If sampling
windows near RefSeq TSSs lifts above 0.497, transcriptional bias
matches the eval distribution.
