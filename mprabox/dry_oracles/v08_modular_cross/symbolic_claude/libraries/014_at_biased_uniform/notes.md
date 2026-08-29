# 014 at_biased_uniform

50k sequences, each char iid from p=(0.4, 0.1, 0.1, 0.4) — AT-biased.

## Result
eval_01 = -0.0001. eval_13 = +0.0036, eval_10 = +0.0024.

## Eval_01 conditions
a=0.0000, b=+0.0054, c=-0.0057.

Condition_c specifically DROPPED with single biased composition (-0.0057 vs +0.0016 dirichlet).
Confirms: it's VARIATION in composition that helps c, not the bias direction itself.

## Conclusion
Composition bias direction (AT vs uniform vs GC) doesn't help eval_01.
Variation in composition (Dirichlet) is what mattered in exp 005.
