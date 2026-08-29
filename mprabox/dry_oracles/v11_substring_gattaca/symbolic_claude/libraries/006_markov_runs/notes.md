# 006 markov_runs

Markov chain with p_stay=0.5 (each char has 50% chance to repeat).

Result: eval_01 mean_r = **0.8333** (vs 0.8526 uniform). Slight drop.
All conditions slightly down.

Within-string runs (autocorrelation) doesn't help; mildly hurts.
Local structure isn't a clear winner.

Next: try narrowing compositional variance (constrained random) to find
the sweet spot between balance and uniform random.
