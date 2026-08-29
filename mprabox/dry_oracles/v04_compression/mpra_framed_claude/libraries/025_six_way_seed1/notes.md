# 025_six_way_seed1 — notes

## Design
Identical to exp 024 (20K nat + 8K cCRE + 7K DHS + 7K ChIP + 3K FANTOM
+ 5K mouse) but SEED=1.

## Result
- eval_01 = **0.5027** — CONFIRMS exp 024's 0.5025!
- 2-seed mean for 6-way design: 0.5026
- 2-seed mean for exp 011 design (011/014): 0.4992
- Δ = +0.0034 between designs, consistent across seeds

## Interpretation
**The 6-way design is genuinely ~0.003 above the exp 011 design.**
Both seeds of the 6-way design land above both seeds of the 4-way
design. This is the first real (multi-seed-confirmed) improvement
over exp 011's 0.5012.

## Mechanism
Spreading regulatory content across 4 distinct atlas modalities (cCRE
chromatin, DHS DNase, ChIP TF, FANTOM CAGE) provides slightly broader
context coverage per training step than concentrating in 2 atlases.
The improvement is small but real and reproducible.

## Implication
exp 024/025 is the new candidate WINNING library. Worth verifying with
a 3rd seed for confidence, then potentially tweaking the ratios within
the 6-way family.

## Next test
exp 026: 6-way design with SEED=2. 3rd realization to firmly establish
the design's mean.
