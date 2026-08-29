# 002 — Motif-enriched library

## What
50k 200bp sequences with 8 canonical strong TF motifs (AP-1, SP1, HNF4, GATA1,
KLF1, E-box, NF-kB, etc.) inserted on random background.

## Why
Test whether prepare.py rewards per-sequence regulatory activity. Prediction:
if yes, mean_r jumps above 0.12 (random baseline), especially K562 (was ~0).

## Result
```
eval_01: mean=0.1146  K562=-0.0032  HepG2=0.1547  SKNSH=0.1922
(other evals 0.106-0.116; eval_08 still outlier at 0.049)
```
Runtime: 15s prepare, 46s wall.

## Interpretation
Motifs did NOT help — slightly hurt eval_01 (0.1185 → 0.1146). K562 dipped
slightly negative. This strongly suggests the score is NOT rewarding
per-sequence activity in the canonical MPRA sense.

This is a big update. Reject H1 (per-sequence activity reward).

Possible explanations for what is being scored:
- Library-level statistics / distribution match to a reference
- Per-row correlation with a hidden target ordering
- Score might be largely independent of sequence content (some structural
  property of prepare.py)

## Next
Run a control: 50k identical sequences. If score is similar → library
content barely matters. If score collapses → content matters but motifs
weren't the right axis.
