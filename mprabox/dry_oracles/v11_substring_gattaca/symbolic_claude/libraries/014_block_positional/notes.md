# 014 block_positional

[43,57] composition + sorted-then-shuffled-within-blocks (4 blocks of 50, each
internally shuffled but block 0 contains mostly 0s, block 1 mostly 1s, etc.).

Result: a=NaN, b=NaN, c~0.66 (down from 009's 0.88).

INSIGHT:
- conditions a and b require per-position VARIANCE across the library.
  Block structure makes per-position distributions heavily biased
  (some positions never see certain chars across the library) → constant
  per-position features → NaN.
- condition c also drops (0.88 → 0.66), suggesting c involves something
  beyond pure character composition. Likely k-mer / dinucleotide features
  also matter for c. Block structure biases dinucleotide composition.

DESIGN RULE: each position must have uniform-ish distribution across the library.
Random shuffle (as in 009) is the right choice.
