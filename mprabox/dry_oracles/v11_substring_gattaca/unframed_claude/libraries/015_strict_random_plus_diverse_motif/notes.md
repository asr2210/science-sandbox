# 015 — 25k strict + 25k (random + 1 motif from 9-pool, diverse)

## Result
- eval_01 mean=**0.8412** (K562 0.839, HepG2 **0.813**, SKNSH 0.871)
- HepG2 collapsed (-0.10 vs 014).

## Interpretation
Diverse motif pool with varying lengths and compositions crashes HepG2.
Confirms 006/008 pattern: HepG2 is brittle when sequences carry varied
biological motifs of varying length. Likely the predictor's HepG2 head
relies on the random uniform structure being undisturbed.

## Lesson
**Motif diversity hurts**; consistent low-variance inserts work.
