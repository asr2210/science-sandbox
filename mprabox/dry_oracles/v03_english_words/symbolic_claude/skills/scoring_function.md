# Scoring function notes

## What we know
- Metric: **Pearson correlation r**. Constant inputs → NaN.
- Score is mean_r ≈ (condition_a + condition_b + condition_c) / 3.
- 14 eval sets. Several are duplicates for the same input:
  - eval_01 == eval_14
  - eval_02 == eval_05 (close-but-different from eval_06)
  - eval_03 == eval_12
  - eval_04 == eval_09
  - Possibly more.
- Uniform random IID baseline: mean_r ≈ 0.42, range 0.379–0.427 across evals.
  - eval_08 is the lowest at 0.3788 (most "sensitive" or hardest eval).
- Random baseline: condition_a ≈ 0.59, b ≈ 0.62, c ≈ 0.05.
  - condition_c is the biggest opportunity (low baseline).

## What we don't know
- What the three conditions are
- What the model architecture is
- What the "true" targets are
- The mapping {0,1,2,3} ↔ A,C,G,T (assuming DNA)

## Hard requirements
- 50,000 lines, exactly 200 chars per line, alphabet {0,1,2,3}
- Must have variance in model predictions (no all-same sequences)
- Time budget: ~2 min per evaluation including I/O
