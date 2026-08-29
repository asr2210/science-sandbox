# 026 slide6_aug

**Design:** 6 windows × 8.33k regions at offsets {-90, -54, -18, 18, 54, 90}.

**Result:** eval_01 = 0.0747 (vs 020's 0.0764). Worse.

**Lesson:** more views per region (6) reduces diversity (only 8.33k unique regions). 020's 4×12.5k is a better balance. Fewer regions is the dominant cost.
