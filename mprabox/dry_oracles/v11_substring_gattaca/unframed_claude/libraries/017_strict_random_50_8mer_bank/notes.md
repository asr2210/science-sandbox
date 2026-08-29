# 017 — 25k strict + 25k (random + 1 8-mer from 50-bank)

## Hypothesis
Larger insert bank → more random-half micro-clusters → bigger lift.

## Result
- eval_01 mean=**0.8820** (K562 0.862, HepG2 0.912, SKNSH 0.872)
- vs 016 (9-bank): mean +0.0015 — small but new best.

## Interpretation
Bank size axis gives marginal positive returns. More bank entries help
slightly but saturate quickly.

## Next
- 018: longer (16-mer) inserts at 50-bank.
- 019: insert in both halves (strict too).
