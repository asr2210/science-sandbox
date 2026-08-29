# 004 GC-only random

50K random sequences over {1,2} only.

## Result
- eval_01: 0.0190 (massive drop)
- Restricting alphabet to {1,2} destroys score.
- Possibly oracle was trained on data spanning all 4 chars; with only 2,
  learner can't disambiguate.
