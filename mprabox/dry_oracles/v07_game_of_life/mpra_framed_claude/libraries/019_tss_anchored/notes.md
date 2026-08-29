# Experiment 019 — TSS-anchored (PLS only)

## Design
50K windows centered around cCRE PLS (Promoter-Like Signature)
elements, ±85bp jitter. 20K unique PLS in hg38; library uses 2-3
passes with different jitter offsets.

## Result
- eval_01: **0.3617** — CATASTROPHIC (Δ -0.026 vs nat, -0.032 vs mix)
- K562: 0.5571, HepG2: 0.3937, SK-N-SH: 0.1343
- Even worse than dinuc-shuffled natural (0.3733).

## Interpretation
Second example of "single regulatory class collapse" pattern (exp 011
TF-diversity was the first). PLS elements are a narrow slice (~20K
unique loci, very high GC, very similar contexts — all promoter-like).
Training on only this collapses the training distribution and the
model fails to generalize.

Library scale ~50K becomes effectively much less when there are
only 20K unique anchors. Combined with the narrow GC/context
distribution → drop of 0.025+.

## Theory refinement — T8 + T9 (collapse)
T8: GC composition balance lifts to 0.394 ceiling.
T9: **Concentrating on any single regulatory class (PLS only, TF-
dense only) collapses distribution and crashes generalization
by 0.02-0.03.** This is a hard floor below natural baseline.

## Catalogue of failure modes
| design | eval_01 | failure mode |
|---|---|---|
| random uniform (008) | 0.369 | no composition |
| dinuc shuffle (007) | 0.373 | no motif structure |
| **PLS only (019)** | **0.362** | **single-class collapse** |
| TF-density (011) | 0.383 | regulatory excess |

PLS-only is worse than dinuc-shuffle. Drives home that bad
library design can actively HURT mean_r below random baselines.

## Next direction
Test species expansion: GC-stratified human + GC-stratified mouse.
Does multi-genome training under controlled composition help?
