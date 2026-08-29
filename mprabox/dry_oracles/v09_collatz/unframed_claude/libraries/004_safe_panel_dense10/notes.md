# 004 — safe 002 panel at density 10

**Hypothesis**: increasing density with the working panel will improve score (if density doesn't hurt).

**Design**: identical motif panel to 002, but 10 inserts per sequence instead of 6.

**Result**: eval_01 = **0.2453** (DOWN from 002's 0.2675 by 0.022).

**Interpretation**: density 10 is worse than density 6 even with proven motifs. The peak appears to be around 4-6 motifs/seq. Score drops monotonically as we add more.

Two non-exclusive theories for *why*:
- (variance) `mean_r` is Pearson correlation across our 50k sequences. Adding lots of motifs to every sequence reduces *variance* in predicted activity → reduces correlation. A library where activity varies more (some no-motif, some heavy-motif) should score higher.
- (over-saturation) The model has diminishing returns on motif content per sequence: extra motifs add noise without adding signal.

**Next**: Exp 005 = mixed-density library (subsets with 0, 3, 6, 9, 12 motifs) to test variance hypothesis. Big win if it beats 0.27.
