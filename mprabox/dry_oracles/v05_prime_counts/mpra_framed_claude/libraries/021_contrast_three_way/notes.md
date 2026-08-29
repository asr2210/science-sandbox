# Exp 021 — 20K gene-desert + 20K random hg38 + 10K cCRE

## Design
Explicit activity-tier contrast. GC=0.420.

## Result
**eval_01 = 0.0489; HepG2 = 0.0559.** Tied with 013 / 020 / 016 within
noise.

| design | eval_01 | HepG2 |
|--------|---------|-------|
| 010 random | 0.0480 | 0.0526 |
| 013 (rand+cCRE) | 0.0493 | 0.0535 |
| 016 desert | 0.0479 | 0.0556 |
| 018 desert+cCRE | 0.0477 | 0.0554 |
| 021 3-way | 0.0489 | 0.0559 |

## Interpretation
Mixing activity tiers gives no lift over 013 alone. The 0.049 eval_01 and
0.054–0.056 HepG2 are the plateau values for any natural-DNA mixture. No
combinatorial design has broken either.

## Theory update
- The eval_01 ≈ 0.05 ceiling is structural. Probably the model's intrinsic
  resolution given 50K x 200bp natural-DNA training and the held-out
  evaluation set distribution.
- HepG2 0.054–0.056 is similarly fixed by mixture design.

## Next step
Try a qualitatively different angle: GC-stratified sampling. Force the
library to span GC composition evenly (12.5K each in 30-40%, 40-50%,
50-60%, 60-70% GC). Real hg38 is heavily skewed toward 40% GC; if the
model is bottlenecked by under-coverage of high-GC sequences, this
should lift performance.

## Time
48s wall, 17s evaluator.
