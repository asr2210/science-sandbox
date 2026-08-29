# 002 — GC composition sweep

## Method
50k sequences as 5 banks of 10k at GC = {20, 40, 50, 70, 85}%.

## Results
mean_r ~ 0.002–0.005 across evals. Tiny but consistently positive.
Compared to random (~0 with sign noise), the shift is real but small.
eval_13 mean_r: -0.0026 → +0.0038, HepG2 at +0.0136.

## Implications
- Composition is at most a minor factor.
- The cross-bank variance in GC content gives non-trivial total
  variance, so any model that correlates with GC content gives a small
  positive r. But the effect is tiny.
- Bigger lever needed. Hypothesis: TF motif content matters far more
  than bulk composition.
