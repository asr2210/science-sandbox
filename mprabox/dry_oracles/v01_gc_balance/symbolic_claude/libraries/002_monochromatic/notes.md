# Exp 002 — Monochromatic composition probe

## Design
12,500 copies each of "0"*200, "1"*200, "2"*200, "3"*200 (50K total).

## Result
All evals returned NaN. The harness emitted many `ConstantInputWarning`
from scipy.stats.pearsonr ("An input array is constant; the correlation
coefficient is not defined").

## Insight (big one)
- "mean_r" is a Pearson correlation, not a normalized score.
- The eval pipeline computes a correlation that **requires variance** in
  the input. With identical sequences, some axis becomes constant.
- Most likely: the eval computes per-sequence the Pearson r between a
  predicted activity vector and a measured activity vector across some
  internal axis (e.g., positions, conditions, replicates). For an
  identical batch of sequences the predicted vector is constant in that
  axis → undefined r.
- This explains why uniform random scores ~0.48: random sequences have
  enough internal structure to yield a moderately well-defined per-seq r.
- It also explains why eval_08 is much lower (0.16) — likely a more
  stringent correlation target or different normalization.

## Rule of thumb (skill update)
DO NOT submit libraries with identical or near-constant per-sequence
predictions. Each sequence needs internal variance for the scoring axis.
Safest interpretation: every sequence must be distinct AND structurally
varied (no constant runs of one character for the full length).
