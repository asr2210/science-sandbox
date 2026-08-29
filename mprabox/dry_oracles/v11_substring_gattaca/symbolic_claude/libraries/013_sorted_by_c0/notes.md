# 013 sorted_by_c0 — diagnostic

Same library as 009 ([43,57] uniform-tuples) but sequences sorted by count of '0'.

Result: eval_01 mean_r = **0.8820** — IDENTICAL to 009 to 4 decimals.

CONCLUSION: Library row order does NOT matter. The eval computes Pearson r
over the library as a SET, not paired indices. So we should optimize the
*distribution* of sequences, not the order/pairing.
