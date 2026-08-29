# 005 dirichlet_compositions

50,000 sequences, each from p_i ~ Dirichlet(0.5,...,0.5), drawn iid.

## Result
eval_01 = 0.0030 (barely above baseline 0.0013).
eval_13 = 0.0045, eval_03/12 = 0.0043. Some evals positive, others negative (04/09=-0.0062, 07=-0.0057).

## Interpretation
Composition diversity alone doesn't substantially move the needle.
Different evals respond differently — composition spread benefits some, hurts others.
The hidden T likely depends on more than overall composition.

## Next
Try k-mer repeats (specific local structure) and motif insertions.
