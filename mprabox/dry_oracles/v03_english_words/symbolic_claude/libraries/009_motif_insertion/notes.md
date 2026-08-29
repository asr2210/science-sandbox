# 009 — motif insertion

iid random seed=42. For half the sequences (25K), positions 95-98 set to "1212".

## Result
- eval_01: mean_r = 0.4197 (vs 0.4200 baseline 001 — same seed) — NEUTRAL
- a=0.5886, b=0.6189, c=0.0517

All values within 0.001-0.003 of baseline. The motif insertion is invisible
to the eval.

## Interpretation
- The eval is INSENSITIVE to small (4-position) structural changes.
- Affects only 1% of total positions (4 × 25K / 10M).
- Either too few changes or eval doesn't care about per-position motifs at this scale.

## Conclusion
Single-motif insertion isn't useful. Need bigger structural changes (which we know hurt) or different strategy.

## Status: 9/30 used
