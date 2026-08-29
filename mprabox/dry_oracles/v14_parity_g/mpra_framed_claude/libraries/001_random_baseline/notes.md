# 001 — Random uniform sequence baseline

**Predicted:** ~0.0 to 0.2 mean_r (low — no learnable structure).

**Got:** mean_r essentially 0 across all 14 evals (range -0.0064 to +0.0010).

**Interpretation:** Random sequences contain no information about regulatory grammar. The model cannot learn anything from them. This confirms the floor.

Runtime: 79s wall (48s eval).

**Next:** Need real genomic sequences with regulatory grammar.
