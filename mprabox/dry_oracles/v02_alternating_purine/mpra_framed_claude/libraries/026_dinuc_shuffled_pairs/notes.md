# Experiment 026 — per-positive dinucleotide-shuffled negatives

## Design
- 013 ratio positives: 15K uniform + 5K CTCF + 5K DNH3
- 25K negatives: each positive's own sequence dinuc-shuffled
- Removes ALL spatial structure (motif arrangement) while preserving
  composition exactly

## Result — mean_r 0.142 (worse than 013's 0.166)
- eval_10 CRATER → 0.097 (lowest seen for eval_10)
- eval_06/11 = 0.174 (013=0.218, lost 0.044)
- eval_07 = 0.155 (mildly down from 0.177)
- eval_13 = 0.139 (slight lift)

## Interpretation
Shuffled-pair negatives are TOO EASY — composition matches but
structure is destroyed, so the model learns "is this genomic-looking?"
rather than "is this regulatory?".
- eval_10 (real-flank-context): tanks because model never sees true
  genomic contrast structure.
- eval_06/11: degraded but not destroyed (rare types still help).

Synthetic negatives (017 Markov: 0.149, 026 per-pos shuffled: 0.142)
ALL underperform real flanks. **Real genomic context is essential.**

## Next
027 = test whether SCALE matters. 013 at 50K is one budget. Try
larger uniform pool: 18K uniform + 4K CTCF + 4K DNH3 + 24K flanks
(slight uniform shift, keep ratios near 013). Tests if 13:15K is
the saturation point or if more uniform helps.
