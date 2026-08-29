# Exp 013 — AT-rich palindromes (combine attempt)

## Design
50K palindromes (length 200), but first-half iid with weights
(0.30, 0.20, 0.20, 0.30). 60% AT, palindromic.

## Result vs baseline + palindrome + AT-iid
| eval    | baseline | exp012 pal | exp007 AT | exp013 AT-pal |
|---------|----------|------------|-----------|---------------|
| eval_01 | 0.4848   | 0.5718     | 0.4669    | 0.4575        |
| eval_07 | 0.5200   | 0.6267     | 0.7117    | 0.7116        |
| eval_13 | 0.4992   | 0.5987     | 0.6900    | 0.6892        |
| eval_04 | 0.4440   | 0.4697     | 0.0890    | 0.0749        |
| eval_08 | 0.1613   | 0.1279     | 0.0418    | 0.0308        |

## Interpretation
**AT-bias dominates and ERASES the palindrome lift on eval_01.**
For eval_07/13, AT-bias was a stronger lever than palindrome, and
palindrome adds nothing on top of AT (07/13 essentially matched
exp 007 AT-iid).

The two effects do NOT combine additively. On eval_01, AT-bias kills
the palindrome benefit (combined 0.458 is worse than either alone).

## Implication
For PRIMARY eval_01, PURE palindromes (exp 012, 0.572) remains best.
For biology evals 07/13, pure AT-iid OR pure palindrome reach about
the same ceiling — additive combination didn't push past 0.71.

Next: explore the palindrome design space to find variants that lift
eval_01 above 0.572. The palindrome lift is specifically from
RC-symmetry; if I impose other structures (tandem, etc.), I can test
whether RC is special or any structure works.
