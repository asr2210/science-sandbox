# Experiment 010 — per-sequence balanced 50/50/50/50

## Result
- mean_r=**0.2768**, K562=0.9927, HepG2=-0.1631, SKNSH=0.0009

## KEY FINDING
Killing per-sequence base-composition variation:
- K562: stayed at 0.99 (doesn't care about per-seq composition!)
- HepG2: -0.16 (NEEDS per-sequence GC variation)
- SKNSH: ~0

So HepG2 r is driven by GC variance across the library. K562 reads
something else (k-mer/positional structure). This separates them.

Strategy: maximize per-seq GC variance while keeping library mean ≈ 50%.
That should lift HepG2 without hurting K562.
