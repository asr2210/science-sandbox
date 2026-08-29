# 020 — 2 8-mer inserts at FIXED positions (50, 142) in random half

## Hypothesis
50×50 = 2500 sub-cluster grid > 50 sub-clusters → bigger lift.

## Result
- eval_01 mean=**0.8784** (K562 0.8553, HepG2 0.9126, SKNSH 0.8674)
- vs 017 (1 random-position insert): mean -0.0036. K562 -0.007.

## Interpretation
More clusters doesn't help — fixed positions hurt slightly. Two 8-mers
(16 bp = 8% of seq) at the same locations every time creates strong
position-specific signal that may confuse the model or reduce effective
diversity in the random background.

## Lesson
Insert axis is saturated near 0.882. 1 random-position 8-mer is optimal.

## Next
- 021: explore orthogonal second-mode designs (alternative to pure random).
