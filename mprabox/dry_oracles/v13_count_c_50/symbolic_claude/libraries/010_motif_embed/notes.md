# 010 motif_embed

Dirichlet(2.0) background with embedded per-sequence random motifs.

## Result
- eval_01: 0.3904 (basically tied with alpha=2.0's 0.3917)
- No improvement from added k-mer variance

So predictors don't seem to reward motif content beyond what composition already
captures. Composition variance is THE main axis we've found.
