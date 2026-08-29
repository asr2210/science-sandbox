# Exp 029 — per-row Dirichlet over all 4 offsets

## Result
eval_01 = 0.1658 (+0.003 over Exp 027). NEW BEST.
condition_a/b = 0.0362 (vs 0.0314 in Exp 027). LIFTED.
condition_c = 0.4251 (essentially same).

eval_06 = 0.2164 (highest seen).

## Interpretation
Adding per-row p variation (via 4-way Dirichlet) lifts condition_a/b
without affecting c. a/b are sensitive to per-row composition variance.
c is sensitive to per-row noise direction variance.

## Next (final experiment)
Push further: α=(0.7, 0.1, 0.1, 0.1). Same mean p=0.7 but maximum
per-row variance (precision 1, std 0.32). Test if more extreme per-row
variation continues to lift, or hits diminishing returns / regression.
