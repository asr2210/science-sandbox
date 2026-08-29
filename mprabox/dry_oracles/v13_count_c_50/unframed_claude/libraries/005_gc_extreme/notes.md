# 005_gc_extreme

## What
50K sequences with GC% uniformly in [0.05, 0.95]. Realized std=0.262 (vs 0.177 for exp 4).

## Why
Test whether monotonic improvement continues with wider GC range.

## Results
eval_01: **0.4139** (vs exp 4: 0.392, vs random: 0.156)
- K562_r: 0.472 (vs 0.447)
- HepG2_r: 0.363 (vs 0.348)
- SKNSH_r: 0.407 (vs 0.382)

Modest +5.6% gain from doubling GC std. Diminishing returns.

## Interpretation
GC variance alone has limited ceiling around 0.41 on eval_01. Need an orthogonal axis to make further progress. Likely candidates: dinucleotide composition (especially CpG), k-mer composition, or naturally-distributed multi-feature variation.

eval_08 still dropping (0.20). It's anti-correlated with compositional spread.
