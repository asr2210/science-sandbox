# 006 — Scaffold length 100 (period-4)

Same as 005 but scaffold doubled to 100 chars.

## Result — STRONG NEGATIVE
- eval_01: -0.149 (vs +0.27 at length 48)
- c FLIPPED: +0.65 → -0.65
- b kept rising: +0.10
- a slightly down: 0.097
- Composition still balanced

## Interpretation
Past some threshold, condition c reverses sign sharply. Likely a
nonlinear penalty for excessive periodic / structured content.
b appears to scale monotonically with cross-sequence alignment
within the tested range.

The optimum is between scaffold length 48 and 100.
Need to also test whether periodicity itself is the trigger or
whether ANY long scaffold (random fixed) would flip c.
