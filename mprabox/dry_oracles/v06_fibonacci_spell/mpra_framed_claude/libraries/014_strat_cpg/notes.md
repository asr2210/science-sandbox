# 014 — CpG-density stratified chr22 windows

## What I tested
50k chr22 200bp windows stratified into 5 equal-quantile CpG-count
bins (CpG ranges: 0-1, 1-2, 2-3, 3-5, 5-49 occurrences per 200bp),
10k per bin. Random orientation. Seed=42.

## Result — basically tied with 012, mixed wins
- eval_01 = 0.1361 (012: 0.1367, -0.0006)
- mean of evals = 0.1299 (012: 0.1308, -0.001)
- eval_07 = **0.1310** (012: 0.1282, +0.003 — new max for eval_07)
- eval_04 = **0.1385** (012: 0.1360, +0.003 — new max for eval_04)
- K562 on eval_07: 0.049 (012: ~0.037 — large jump)
- K562: 0.037 overall, HepG2: 0.174, SK-N-SH: 0.198

## Critical observation
CpG bins are highly correlated with GC: mean GC per CpG bin =
0.39 / 0.43 / 0.46 / 0.50 / 0.56. So this experiment is essentially
GC-stratification by proxy. CpG is NOT meaningfully orthogonal to
GC at this granularity.

That CpG-stratification slightly LOSES on eval_01/mean but WINS on
eval_04, eval_07, eval_09 suggests:
- Different evals reward slightly different compositional emphases
- CpG-density correlates with promoter-like sequences that help K562
  (hematopoietic; eval_07 K562 jumped +0.012)

## Theory update
A single-axis stratification (whether GC or CpG) hits a ceiling
near eval_01=0.137. To progress I need either:
1. Joint stratification on truly-orthogonal axes
2. More compositional pool (multiple chromosomes)
3. Functional enrichment (promoters / CpG islands directly)
4. Larger compositional range (synthetic interpolation, mutagenesis
   from a stratified base)

## What to try next
015: Joint GC stratification across chr19+chr22. Chr19 is the most
GC-rich human chromosome (mean GC ~0.48 like chr22 but with much
more GC-rich tail). Stratifying across the combined pool gives
broader GC range and 2x more candidate windows, which may extend
the compositional tail beyond what chr22 alone can offer.
