# Experiment 030 — finer GC stratification (10 bins)

## Design
50K natural windows, 5000 per 10 GC bins:
[0, .25, .30, .35, .40, .45, .50, .55, .60, .65, 1.0].

## Result
- eval_01: 0.3916
- K562: 0.6024, HepG2: 0.4274, SK-N-SH: 0.1450

## vs 5-bin GC-strat (014)
- 5 bins (10K each): 0.3939
- 10 bins (5K each): 0.3916
- Δ: −0.0023 (~2σ)

Slightly lower. Higher-resolution GC binning doesn't help; smaller
per-bin samples may actually hurt slightly. 5-bin resolution was
already saturating the GC lever.

## Conclusion
**GC stratification at 5 bins is the right resolution.** No additional
gain from finer binning, and possibly small loss from sample
dilution per bin.
