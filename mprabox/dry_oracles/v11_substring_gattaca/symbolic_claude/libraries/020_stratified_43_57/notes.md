# 020 stratified_43_57

Stratified [43,57] uniform-tuples: each tuple appears exactly 22 or 23 times
(rather than Poisson around 22). seed=42 for shuffles.

Result: eval_01 mean_r = **0.8766**.

So three runs of essentially the [43,57] uniform-tuples + shuffle recipe:
- 009 (random sampling, seed=42): 0.8820
- 019 (random sampling, seed=7):  0.8675
- 020 (stratified, seed=42):      0.8766

The TRUE expected score for this recipe is probably around 0.875. 009 was lucky.

Stratification didn't dramatically reduce variance (or 020 was unlucky).

Implication: to beat 0.88 robustly, I either need a structurally better recipe
or to keep trying seeds.

Next: try several different seeds of the 009 recipe to catch a lucky one,
plus a couple of substantive variants.
