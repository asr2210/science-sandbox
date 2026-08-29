# Exp 003: Positional gradient

## Setup
Sequence i drawn iid from {0,1,2,3} with triangular weights centered at c_i = 3*i/(N-1).
"Average char value" of seq_i ramps linearly from 0 to 3 as i goes from 0 to N-1.

## Results
Most evals scored LOWER than random:
- eval_01: 0.0648 → 0.0519 (down)
- eval_07: 0.1310 → 0.0885 (down)
- eval_08: 0.0563 → 0.0270 (~halved)
- eval_13: 0.1186 → 0.0895 (down)
- eval_04/09: 0.0813 → 0.0493 (down)
- eval_10: 0.1194 → 0.0594 (~halved)

Pairs still match: (01,14), (02,05), (03,12), (04,09), (06,11). Confirms eval-pair structure.

## Theory update
Position-INDEX correlation hypothesis REJECTED — adding positional structure HURT all scores.

This suggests:
- The score is computed per-SEQUENCE (not across position index)
- Sequences with biased composition have lower per-seq variance, reducing |r| with a fixed-target sequence
- Random gives slightly higher score because per-seq features are more spread

**Working hypothesis**: per-sequence pearson r between my_seq vector and a hidden target sequence (or hidden model output of the same length).

## Next
Exp 004: send 50K copies of ONE non-constant sequence. This tests per-sequence vs per-library:
- If per-seq: score = pearson(seq, target). Well-defined (single number per eval).
- If per-library: score = NaN (no across-sequence variance).
