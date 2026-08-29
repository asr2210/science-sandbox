# Experiment 003 — Row-monotonic '0' gradient

## Setup
- Row i: p_0 = i/(N-1) per position; remaining 1-p_0 split equally over {1,2,3}.
- Avg '0' fraction across library = 0.50 (vs 0.25 for uniform random).

## Results (vs exp 001 random)
- eval_01: mean 0.118 → 0.090. DROP.
- condition_a went UP for many evals (0.009 → 0.017 for eval_01).
- condition_b, c dropped.
- eval_08 still strictest (0.046).

## Interpretation
- Mixed effect. The drop could be from:
  - increased '0' composition hurts (composition matters; '0' is "bad" letter).
  - decreased diversity in {1,2,3} hurts.
  - the row-ordering itself.
- Can't disentangle without an order-only experiment.

## Implication
- Condition_a may be sensitive to row-order. Worth pursuing.
- Conditions b, c seem to like uniform composition.

## Next
Need a clean order-only probe: same per-string composition as exp 001, different row order.
