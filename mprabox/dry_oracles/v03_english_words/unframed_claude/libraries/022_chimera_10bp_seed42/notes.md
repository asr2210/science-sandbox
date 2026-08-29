# Exp 022 — chimera 10bp seed=42 (validation)

**Hypothesis**: Replicate Exp 017 (chimera 10bp insert, mean_r=0.4248)
with a different seed to confirm the +0.013 lift over random is robust.

**Result**: eval_01 = 0.4202.

**Comparison**:
| seed | pure random | chimera 10bp |
|------|-------------|--------------|
| 0    | 0.4203 (Exp 001) | — |
| 17   | — | 0.4248 (Exp 017) |
| 42   | 0.4235 (Exp 011) | 0.4202 (this) |

**Interpretation**: Chimera 10bp insert does NOT consistently beat pure
random. With seed=17 it lifted +0.013; with seed=42 it dropped -0.003.
Mean across the 2 chimera seeds = 0.4225; mean across 2 random seeds =
0.4219. Difference (+0.0006) is well below the noise floor (±0.003).

**Takeaway**: Exp 017 was lucky seed noise. The chimera-insert approach
does not produce a robust improvement. Pivot strategy: explore the
random-baseline neighborhood (slight composition shifts, multiple seeds,
distribution sweeps) to find what *actually* moves the metric.
