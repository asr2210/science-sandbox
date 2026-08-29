# Experiment 011 — 32-motif pool, 1 per seq, random pos

## Result
**eval_01: 0.331 → 0.344 (+0.013, above noise floor).**
Every single eval improved or held flat:
- eval_07: 0.420 → 0.459 (+0.039)
- eval_13: 0.400 → 0.442 (+0.042)
- eval_04/09: 0.301 → 0.324 (+0.023)
- eval_06/11: 0.351 → 0.368 (+0.017)
- eval_10: 0.383 → 0.397 (+0.014)
- eval_03/12: 0.357 → 0.370 (+0.013)
- eval_01/14: 0.331 → 0.344 (+0.013)
- eval_08: 0.109 → 0.103 (~noise)

## Interpretation
First library to beat random uniform on eval_01. Critical factors:
- LARGE motif pool (32) → each motif in only ~1500 seqs (3% of library) → no single motif dominates library statistics.
- ONE motif per seq → preserves per-column near-uniformity (each column gets a tiny fraction of motif content).
- VARIED POSITIONS → no fixed-column variance loss.
- DIVERSE MOTIFS → covers many TF binding "vocabulary tokens" the scorer recognizes.

The scorer rewards regulatory content WHEN it's diverse enough to keep per-motif library frequency low (< 5%).

## Theory update → T8
The scorer's Pearson r benefits from:
(a) Library statistics near uniform random (so it stays in-distribution).
(b) Heterogeneous regulatory content sprinkled across the library at low per-motif frequency.

T8: optimum library = uniform random base + sprinkled diverse motifs at low per-motif frequency.

## Next
Exp 012: 64-motif pool to test if more pool diversity continues helping. If yes, push to 128 or 256.
