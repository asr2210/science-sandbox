# Experiment 006 — Dirichlet(α=1) per-row composition

## Setup
- Per row: p ~ Dirichlet(1,1,1,1) (uniform on 4-simplex).
- Sample 200 positions iid from Categorical(p).

## Results
- eval_01: mean 0.118 → 0.138 (+0.020). IMPROVEMENT.
- condition_a: 0.009 → 0.043 (5x jump!).
- condition_b: 0.156 → 0.170 (modest +0.014).
- condition_c: 0.190 → 0.202 (modest +0.012).

## Interpretation
- Pushing symmetric composition variance helps ALL conditions.
- condition_a benefits proportionally MOST — composition variance is its lever after all.
- condition_b, c near-saturating? Or just need more push.

## Next
Push α lower for more composition variance:
- Exp 007: α=0.3 (more peaked Dirichlet).
- If still improves → try α=0.1 or pure homopolymer mixture.
- If plateaus/drops → there's an optimum near α=1.
