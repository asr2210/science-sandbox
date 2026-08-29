# 018 no_runs

[43,57] composition + greedy NO-same-char-adjacent placement.

Result: a=NaN, c=NaN, b=0.77.

CATASTROPHIC: removing same-char adjacency made a, c constant features (NaN).
- Same-char dinucleotides ("00", "11", "22", "33") are essential features.
- b dropped sharply too (0.91 → 0.77).

Don't aggressively eliminate dinucleotide types. Natural random shuffle distribution
of dinucleotides is needed.

Next: try smaller perturbations to 009 — different seed (noise check), then
explore distributional variants more carefully.
