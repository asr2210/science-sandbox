# Experiment 024 — noise injection

## Design
25K natural hg38 + 25K random uniform DNA (40% GC). Tests whether
adversarial random "negative" examples help generalization.

## Result
- eval_01: 0.3800 (Δ -0.0076 vs nat, -0.015 vs ceiling)
- K562: 0.5842, HepG2: 0.4135, SK-N-SH: 0.1423

## Interpretation
Pure natural = 0.388, pure random = 0.369, 50/50 mix = 0.380.
Approximately the average. **Noise injection is roughly linear:
performance scales with fraction of signal-bearing training data.**

The model is NOT bottlenecked by lack of negatives; it's
bottlenecked by signal volume. Adding 25K random uniform reduces
effective N from 50K to ~25K signal + 25K noise.

## Implication
The model does not benefit from explicit contrast learning via
random "negatives." Train on as much natural-like signal as
possible.

## Next direction (exp 025)
Most informative remaining question: does motif/syntax content
matter at all once GC is controlled, or is GC the whole story?

Test: **GC-stratified random uniform**. Generate random DNA but
bias each window to fall in a specific GC bin (so the library
has uniform GC distribution like exp 014). If lifts to ceiling
→ GC is everything, motifs don't matter. If stays low → motifs
matter even under GC control.
