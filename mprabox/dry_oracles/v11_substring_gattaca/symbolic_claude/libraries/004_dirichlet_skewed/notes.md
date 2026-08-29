# 004 dirichlet_skewed

Each of 50000 sequences: draw probs ~ Dirichlet([0.3,0.3,0.3,0.3]), then sample 200 chars.

Result: eval_01 mean_r = **0.6545** (vs 0.8526 for uniform random). Drop of 0.20!
condition_a dropped most (0.85 → 0.45).
condition_b also dropped (0.87 → 0.76).
condition_c dropped (0.83 → 0.75).

Interpretation: extreme inter-sequence composition variance HURTS r.
The score apparently rewards more uniform compositions across the library
(like uniform random). Adding compositional noise increases std(f)*std(g)
more than cov(f,g), so r drops.

Direction: try sequences with even MORE balanced/uniform compositions (exact balance).
