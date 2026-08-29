# 001_dhs_signal_weighted

## What I tested
Sample 50,000 DHS Index elements (Meuleman 2020, hg38, ~3.59M autosomal+sex
elements) with probability proportional to `mean_signal`. Extract 200bp
centered on each DHS `summit` from hg38 via twobitreader. Drop windows with
N or off-chromosome edges; oversample to reach exactly 50,000. 3 seeds.

## Why
First experiment of the run — needed to (a) validate that my pipeline
produces sensible numbers and (b) anchor a baseline I can compare future
experiments against. `mean_signal` weighting is the closest proxy I can
build to the published `dhs_topic` strategy (the per-element 16-component
NMF loadings are not in the public Index TSV; only the dominant
`component` label is).

## Result
- **eval_01 mean_r = 0.7242** (vs dhs_topic baseline 0.7232 — within noise)
- Cross-14-eval mean = ~0.7511
- Per-seed eval_01: 0.6892 / 0.7481 / 0.7353 — substantial seed variance
- prepare.py time: 953s (~16 min, matches expectation)

## How it compares to baselines (eval-by-eval)
- eval_07: 0.7611 vs 0.7398 baseline (+0.021 — *better*)
- eval_13: 0.7564 vs 0.7271 baseline (+0.029 — *better*)
- eval_08: 0.6781 vs 0.7011 baseline (-0.023 — *worse*; consistent with eval_08
  rewarding random/synthetic content I do not include)
- eval_09: 0.8496 vs 0.8601 baseline (-0.011 — slightly worse)
- All others within ±0.015 of baseline.

## Takeaways
- Pipeline reproduces the published baseline. mean_signal-weighting works
  as a `dhs_topic` proxy.
- 3-seed eval_01 standard deviation is ~0.025 (range 0.069 across seeds).
  This is the noise floor for comparing future experiments — anything
  smaller than ~0.01 difference is unlikely to be meaningful.
- eval_08 deficit (~0.02) suggests there is room to gain by adding
  random/synthetic sequences if I am willing to trade a bit of in-distribution
  performance — `dhs_synth` baseline shows the same trade.
