# Exp 016 — period-16 all-phases template

## Design
Template = (0,1,2,3, 1,2,3,0, 2,3,0,1, 3,0,1,2) repeated. Each 4-block
is a different phase of (0,1,2,3). p=0.7.

## Result
eval_01 = 0.0996 — worse than baseline. condition_c ≈ 0.28. All evals
dropped together: no eval benefited from the multi-phase template.

## Interpretation
Mixing phases within ONE template dilutes the signal everywhere.
Each eval prefers a specific phase; covering all phases simultaneously
gives partial credit nowhere.

## Next direction
Stay on (0,1,2,3) period 4 at p=0.7 as the best pattern. Try
**asymmetric noise**: per position the template-base at 0.7, the
*next-in-cycle* base at 0.2, the other two at 0.05 each. If the
hidden template has secondary-structure preference (next-base also
weakly preferred), asymmetric noise should outperform symmetric.
