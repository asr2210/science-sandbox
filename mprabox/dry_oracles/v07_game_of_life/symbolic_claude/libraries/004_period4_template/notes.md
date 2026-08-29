# 004 — Periodic template test

4 blocks (12.5k each):
- period 4: "0123" repeated, 30% noise
- period 8: "00112233" repeated, 30% noise
- period 2: "0101", 30% noise (only chars 0,1)
- blocks of 50: 50x"0",50x"1",50x"2",50x"3", 30% noise

## Results (vs baseline 0.3943)
- eval_01: 0.1563 (DROP 0.24)
- eval_13: 0.1770
- eval_08: 0.1345
- All evals dropped enormously.

## Interpretation
Periodic structure is HEAVILY penalized. This is stronger evidence that the
function rewards entropy/randomness rather than alignment with simple patterns.

Confounders:
- Period-2 block has only chars {0,1}, so low compositional diversity
- Block-of-50 has long runs of identical chars (low local variance)

But even period-4 "0123" (balanced composition, no long runs) is mixed in.
The mean dropped by 0.24 — too big to be from just 1-2 bad blocks.

## Theory update
- Function likely penalizes low-entropy / structured sequences.
- Random uniform is near-optimum at the entropy/composition level.
- To beat random, need to find specific patterns not captured by simple periodicity.

## Next probe ideas
- Isolated period-4 to see if 0123 alone is OK or bad
- Single-char bias for a SPECIFIC char (not averaged over 4) to see if any char is favored
- Position-dependent (non-periodic) targets
- Sub-alphabet tests (e.g., only chars 0,1)
