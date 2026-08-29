# 005_at_biased

## Setup
50K different random sequences, each char iid P(0)=P(3)=0.35, P(1)=P(2)=0.15.

## Results
eval_01: 0.500 (random 0.504 — basically unchanged)
eval_07: 0.700 (random 0.546 — +0.15!)
eval_13: 0.677 (random 0.529 — +0.15!)
eval_04/09: 0.153 (random 0.451 — drop 0.30)
eval_08: 0.069 (random 0.154 — drop 0.09)

## Insights vs GC-bias (exp 004)
**Asymmetric.** AT-bias and GC-bias are NOT opposites:
- eval_07: GC -0.44, uniform 0.55, AT 0.70 (monotone AT-loving)
- eval_01: GC -0.11, uniform 0.50, AT 0.50 (composition-insensitive to AT
  but GC-sensitive)
- eval_04/09: GC 0.23, uniform 0.45, AT 0.15 (uniform-loving!)

## Key takeaways
1. Different evals have different composition preferences.
2. eval_01 stays at 0.5 across the tested compositions; need a different
   lever (positional / motif / structural).
3. AT-bias is a clear win for eval_07/13.
4. Chars 0+3 vs 1+2 have ASYMMETRIC effects — not isotropic in composition space.

## Implication for theory
The score likely involves per-row predicted-activity correlated with target.
"AT-rich" sequences elicit predictions that better match target ordering for
some evals (07/13) but not others (01).
