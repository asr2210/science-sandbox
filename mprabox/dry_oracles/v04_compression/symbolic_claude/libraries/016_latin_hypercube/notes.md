# 016 Latin Hypercube (positional balance)

Each of 200 positions has exactly 12,500 of each character.
Per-seq composition still binomial (similar to iid).

## Result
- eval_01 = 0.3134. Within noise of iid uniform.
- Positional exact balance does not clearly help.
- Confirms learner cares about full library distribution, not positional uniformity.
