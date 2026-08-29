# 004 — All 50K sequences identical

## Result
NaN for every eval. Constant input warning from `eval/harness.py:111`.

## Critical insight
This **confirms** the scoring is Pearson correlation between a per-sequence value and a per-sequence target. If all my sequences are identical, the input variance is zero → r undefined.

So `prepare.py` produces ONE value per sequence (or possibly per-cell-line) and correlates with hidden ground truth. The hidden ground truth must be either:
- Computed by an oracle on each of my sequences (so it varies with sequence content)
- Indexed by sequence position (test sets have fixed per-index targets)

If indexed by position, then any variable library should produce a fixed score. But we saw libraries' scores vary, so it can't be purely position-indexed.

Most likely: there's a hidden function `f_oracle(seq)` that gives true activity per sequence, and a learned model that tries to predict it from sequence. The Pearson r is between the learned model's predictions on held-out test sequences and their true activities. The library quality determines how well the learned model generalizes.
