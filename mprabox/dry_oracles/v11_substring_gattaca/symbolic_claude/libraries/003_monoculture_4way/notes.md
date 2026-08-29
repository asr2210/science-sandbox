# 003 monoculture_4way

12500 each of "0"*200, "1"*200, "2"*200, "3"*200.

Result: still NaN for all evals.

But notably only 2 warnings (vs 42 in exp 002). So most internal correlations
are valid now (have variance), but a few are still constant, and NaN propagates.

Suggests: the score is aggregated from many sub-correlations (perhaps positional
or k-mer-based). Per-position features (e.g., "char at position 50" or "count
of dinucleotide 01") are constant within a monoculture group, and constant across
the library if all sequences fail to produce variance in that feature.

Therefore: per-sequence variance (each sequence containing all 4 chars in mixed
order) is likely required for the scoring to compute valid r values.
