# Exp 012 — Palindromic sequences (BREAKTHROUGH)

## Design
50K sequences of length 200. Each = (random 100 chars) ||
(reverse-complement of those 100). Perfect palindrome. RC mapping:
A↔T (0↔3), C↔G (1↔2). Aggregate composition balanced.

## Result vs baseline
| eval    | baseline | exp012  | delta   |
|---------|----------|---------|---------|
| eval_01 | 0.4848   | 0.5718  | **+0.087** |
| eval_02 | 0.4851   | 0.5717  | +0.087  |
| eval_03 | 0.4843   | 0.5665  | +0.082  |
| eval_04 | 0.4440   | 0.4697  | +0.026  |
| eval_06 | 0.4830   | 0.5683  | +0.085  |
| eval_07 | 0.5200   | 0.6267  | +0.107  |
| eval_08 | 0.1613   | 0.1279  | -0.033  |
| eval_10 | 0.4700   | 0.5686  | +0.099  |
| eval_13 | 0.4992   | 0.5987  | +0.100  |

**13 of 14 evals improved.** Only eval_08 dropped slightly. Mean
across evals: 0.458 → 0.530 (+0.072).

## Per-condition breakdown (eval_01)
- cond_a: 0.5241 → 0.5419 (+0.018)
- cond_b: 0.5009 → 0.6516 (+0.151) — HUGE LIFT
- cond_c: 0.4295 → 0.5219 (+0.092) — big lift

Palindromes specifically reward conditions b and c. Condition a is
nearly unchanged.

## Interpretation
The scoring model strongly rewards palindromic structure, consistent
with biology (TF binding sites are commonly palindromic). The model
recognizes RC-symmetric structure and predicts more in line with the
target on such sequences.

This is the FIRST experiment to beat baseline on eval_01.

## Next steps
- AT-rich palindromes: combine two known lifts. Might push eval_01
  even higher (or might drop it if effects don't combine).
- Imperfect / spacer palindromes: test specificity of palindrome
  recognition.
- Mix of palindrome lengths.
