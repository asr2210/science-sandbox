# Local uniformity is required

**Rule:** Every position in every sequence should be drawn from the same
local distribution. Any heteroscedasticity — across sequences, within
sequences, or via local runs — wrecks the model's mean_r by 0.04+.

## Evidence
- **exp 011:** Mixed GC=0.5 and GC=0.6 across sequences → 0.756 (vs 0.857
  for uniform-GC=0.55). Catastrophic.
- **exp 005:** Per-sequence GC ~ Uniform[0.2, 0.8] → 0.741. Same lesson.
- **exp 017:** TpA depletion forced T[A→A]=T[T→T]=0.50, creating local
  polyA/polyT runs → 0.819 (vs 0.868 baseline). Catastrophic.

## Why
The training-time activity model expects each sequence's local context
to be drawn from one stationary distribution. When local stats vary,
the model can't form a consistent sequence→activity mapping.

## Practical thresholds
- Single-base self-transition T[x→x] > 0.4 → polyrun risk → avoid.
- Cross-sequence composition stddev (e.g., GC stddev > 0.05) → avoid.
- Distributional mixtures (two GC modes) → never.

## What works
- 1st-order Markov chain with all transitions < 0.7 and self-transitions
  ≤ ~0.35. Specifically exp 015 (max single transition 0.65 = T[C→G],
  max self-transition 0.30 = T[A→A]) was fine.

## Implication for designing biases
To add a new dinucleotide bias, check that the necessary compensating
transitions don't push self-transitions or single transitions over the
threshold. Use 2nd-order Markov for richer structure if a 1st-order
design forces extreme rows.
