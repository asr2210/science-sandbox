# 008 — hybrid: 98% iid + 2% outliers

49,000 iid uniform + 1,000 outliers (250 per char at 90% bias), permuted.

## Result
- eval_01: mean_r = 0.4047 (vs 0.4200 baseline) — slightly WORSE
- a = 0.5773 (down 0.011), b = 0.5885 (down 0.030), c = 0.0482 (down 0.005)

Even small outlier injection hurts. b suffers most. c doesn't improve.

## Conclusion
Outlier injection doesn't help even at 2%. iid random with NO mixing is best.

## Status: 8/30 used
