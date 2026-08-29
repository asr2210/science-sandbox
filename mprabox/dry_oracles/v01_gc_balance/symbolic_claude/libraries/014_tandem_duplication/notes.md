# Exp 014 — Tandem duplication (RC control)

## Design
50K seqs length 200. first 100 iid uniform, second 100 = COPY of first 100.
Identical to exp 012 except RC is replaced by identity.

## Result
| eval    | baseline | tandem (014) | palindrome (012) |
|---------|----------|--------------|------------------|
| eval_01 | 0.4848   | 0.5187       | 0.5718           |
| eval_02 | 0.4851   | 0.5190       | 0.5717           |
| eval_03 | 0.4843   | 0.5195       | 0.5665           |
| eval_04 | 0.4440   | 0.4569       | 0.4697           |
| eval_07 | 0.5200   | 0.5615       | 0.6267           |
| eval_08 | 0.1613   | 0.1677       | 0.1279           |
| eval_13 | 0.4992   | 0.5407       | 0.5987           |

Mean across evals: 0.458 → 0.476 (tandem) → 0.530 (palindrome).

## Interpretation
**RC-symmetry is specifically better than tandem identity.**
Both structures lift the score above baseline (so half-to-half
redundancy alone helps somewhat), but RC roughly DOUBLES the lift
relative to tandem on eval_01:
  tandem:    +0.034
  palindrome: +0.087

This is strong evidence the scoring model is sensitive to a
biologically meaningful palindromic signal (TF binding-site-like).
Tandem duplication doesn't trigger this signal — the model
recognizes the structure as "two-block repeat" but doesn't reward
it the same way.

Interesting wrinkle: eval_08 — tandem helps (+0.006), palindrome
hurts (-0.033). Eval_08 seems anti-palindrome. The two-block
redundancy itself is fine; it's specifically RC that bothers it.

## Implication
- Palindrome (exp 012) remains best on eval_01.
- The mechanism is RC-specific, not generic-structural.
- This narrows the search: improvements should preserve RC
  symmetry. Variants to try:
    - Multiple shorter palindromes per sequence
    - Palindromes with central spacer
    - Imperfect palindromes (some mismatches)
    - Concatenated short palindromes vs one long one
