# 022 slide2_topic25k

**Design:** 25k topic-stratified cCREs (4-mer K-Means(50)) × 2 sliding windows (offsets ±50).

**Result:** eval_01 = 0.0756 — within noise of 020 (0.0764). But notable highs across other evals:
- eval_07 = 0.1467 (NEW BEST)
- eval_13 = 0.1440 (NEW BEST)
- eval_10 = 0.1288 (top tier)
- eval_08 = 0.0638 (close to top)

**Interpretation:** Combining topic diversity (25k diverse regions) with light augmentation (2 views) helps composition-heavy evals (07, 13, 10) but doesn't push eval_01 past 020.

**Lesson:** Different evals respond to different recipes:
- eval_01 prefers: high TFBS-density + slide aug (020)
- eval_07/13: prefers diversity + light slide aug (022)
- The recipes don't add up to one universal winner.
