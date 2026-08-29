# 009_gradient_extreme

## Setup
Same as 008 but min count = 2, max count = 98. Slightly more extreme gradient.

## Results vs 008
- eval_01: 0.6010 (was 0.5949, +0.006)
- eval_07: 0.6685 (was 0.6621, +0.006)
- eval_13: 0.6372 (was 0.6318)
- eval_04/09: 0.5091 (was 0.5002, +0.009)
- eval_08: 0.1216 (still stuck)

## Insights
- Marginal returns confirm: pure composition gradient is saturating.
- Most gain was already extracted at min=5.
- Need to add ANOTHER row-correlated signal to keep climbing.

## Saturation evidence (eval_01 vs min count)
- min=5 (008): 0.5949
- min=2 (009): 0.6010
- delta: 0.006 for going much more extreme
- pushing to min=1 would give maybe +0.003 with NaN risk

## Strategic pivot
Need an orthogonal signal that ALSO correlates with row index. Candidates:
- Per-char independent gradients (chars 0 vs 3 separate axes; 1 vs 2 separate)
- Positional motifs with frequency varying by row index
- Intra-row structural features (e.g., palindromes, runs)
- Embed row-index "barcode" in a few positions
