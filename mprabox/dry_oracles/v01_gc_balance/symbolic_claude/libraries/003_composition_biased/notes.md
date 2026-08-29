# Exp 003 — Composition-biased sub-libraries

## Design
50K sequences = 12.5K each from 4 categorical distributions:
  one char at P=0.55, others at P=0.15.
Each char "biased" in turn (0, 1, 2, 3). Average is composition 0.25 each.

## Result vs baseline (Exp 001)
| eval    | baseline | exp003 | delta  |
|---------|----------|--------|--------|
| eval_01 | 0.4848   | 0.3997 | -0.085 |
| eval_07 | 0.5200   | 0.4622 | -0.058 |
| eval_08 | 0.1613   | 0.1646 | +0.003 |
| eval_13 | 0.4992   | 0.4416 | -0.058 |
| eval_04 | 0.4440   | 0.3117 | -0.132 |

**ALL evals dropped.** No sub-library category produced a lift large
enough to compensate. Composition bias is bad on average.

## Interpretation
- Per-position composition bias HURTS the score.
- Random uniform composition appears near-optimal.
- All conditions (a, b, c) move together — suggests the same underlying
  factor drives all of them.

## Theory update
The scoring likely rewards "natural" sequence diversity. Random uniform
sequences are already a strong baseline — composition shifts reduce it.

Next: probe whether sequence STRUCTURE (autocorrelation, local order)
matters independent of composition. If structure has no effect, then
the score might just be "how close to uniform random per-position".
If structure matters, that's a knob we can turn.
