# Experiment 027: Top-signal pooled cCRE∩DNase intersect

eval_01 = 0.0717. **BELOW plateau** (~0.0744-0.0748).

Selected top-signal-percentile peaks from each cell, pooled, took
top 45K. Per-cell origin: K562 22K, HepG2 8K, SKNSH 15K.

**Key finding:** Top-signal selection HURTS. Likely because the highest
DNase signal peaks are concentrated in housekeeping regions (active
promoters, CpG islands, ubiquitous regulators) which are LESS diverse
than the random sample of intersect peaks in 024.

**Confirmed: diversity > intensity** for MPRA training composition.

Doesn't change leaderboard:
- 019 kitchen-sink: 0.0748 (3-seed mean) ← leader
- 009 hybrid:       0.0746
- 024 intersect:    0.0744
- 027 top-signal:   0.0717 (single)
