# Exp 008 — Promoter-focused library (PLS + pELS cCREs)

## Design
40K PLS (+CTCF-bound) + 10K pELS, 200bp windows centered on element midpoints.
GC = 0.599 (promoters are very GC-rich).

## Result
**eval_01 = 0.0387 — slightly worse than random hg38 (0.052) and tied with
other natural-DNA libraries.** eval_13 = 0.018 (lowest in any natural lib).

| eval | rand | hg38 | cCRE | multi | PLS |
|------|------|------|------|-------|-----|
| 01 | 0.042 | 0.052 | 0.043 | 0.045 | 0.039 |
| 13 | 0.020 | 0.034 | 0.025 | 0.032 | 0.018 |

## Interpretation
Promoter-only is not better than mixed regulatory DNA. The high GC bias
(0.60) of PLS may actually hurt — the model is forced to learn from very
GC-skewed inputs that don't represent the eval distribution well.

The plateau holds: all natural-DNA library variants cluster at eval_01 ≈
0.04–0.05, well above the noise floor (0.003) yet stubbornly flat. The
model can't extract more signal from "more carefully-chosen real DNA."

## Bigger picture
After 8 experiments I have strong evidence that:
- Library design WITHIN the natural-DNA universe barely moves eval_01.
- The noise floor is ~0.003; design effects span ~0.01 (3x noise) but
  never reach a meaningful lift.
- To move the needle I need something qualitatively different.

## Next step
Try motif-DOMINATED synthetic library (each 200bp is ~80% motif content,
not 5%) to test whether motif density helps when no other signal exists.

## Time
11s evaluator, 43s wall.
