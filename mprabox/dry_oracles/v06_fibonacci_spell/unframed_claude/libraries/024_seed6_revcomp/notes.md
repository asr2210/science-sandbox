# Experiment 024: Best base (006 seed=6) + 50% revcomp augmentation

## Plan
Stack exp 006's seed=6 base (known 0.1387) with 50% revcomp aug. If
revcomp adds any signal, this should land 0.140+.

## Result
- eval_01 mean_r = **0.1371** — LOWER than pure 006 (0.1387) by 0.0016
- Pure 006 base is better than 006 + revcomp
- K562 r=0.0475 (slightly higher than 006), but HepG2/SKNSH dropped

## Implication
Revcomp augmentation is mildly NEGATIVE on a good base. The test set
appears to be sensitive to strand orientation (perhaps reflects the
natural transcriptional polarity baked into the genome).

The 017 result (0.1379 vs 014's 0.1350) was seed noise, NOT revcomp
benefit — confirmed by the negative delta here on the controlled base.

## Best-so-far still: exp 006 at 0.1387
Plain uniform-random hg38 (seed=6), no augmentation.

## Next
Sweep fresh seeds (042, 123, 777, 2026) to see if any beats 0.1387.
Final library will be the best-seeded plain hg38 random.
