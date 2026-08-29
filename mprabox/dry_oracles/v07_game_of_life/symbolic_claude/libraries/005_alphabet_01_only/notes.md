# 005 — Sub-alphabet {0,1}-only

50k random sequences using only chars {0,1} (50/50 per position).

## Result
NaN on all evals.

## Interpretation
- Each sequence individually has variance (mix of 0 and 1) — std on integer encoding > 0.
- But chars 2 and 3 are completely absent.
- NaN suggests scoring is per-channel (one-hot encoding), and channels for missing chars have std=0.
- This rules out integer-only encoding for the score.

## Theory update
- **Score is computed on 4-channel one-hot encoding (most likely).**
- For each sequence (or population), every channel must have non-zero variance.
- Practical rule: each sequence must contain at least 1 of each {0,1,2,3}, OR population at each position must include all 4 chars somewhere.

## Two competing models still consistent
1. **Per-sequence**: score = mean over sequences of (avg per-channel correlation with target). NaN if any sequence missing a char.
2. **Population**: score involves cross-sequence statistics at each position. NaN if population at any position missing a char (which is the case here).

Need a distinguishing experiment.

## Next probe
50k copies of one fixed random sequence. Each sequence has all 4 chars. But population
at each position is constant (delta). 
- If finite: per-sequence model. 
- If NaN: population model.
