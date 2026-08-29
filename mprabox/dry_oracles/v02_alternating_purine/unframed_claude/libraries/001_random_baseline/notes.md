# 001 — Random baseline

**Hypothesis**: Random sequences give floor / center of score distribution.

**Method**: 50k uniformly random 200bp from {A,C,G,T}, seed=42.

**Result**:
- eval_01.mean_r = **0.1307**
- K562 = 0.008, HepG2 = 0.008, SKNSH = 0.3761
- All evals show SKNSH ~0.37, K562/HepG2 ~0 (random-level)
- eval_08 is outlier (lower across the board)
- Several eval pairs are identical: 01=14, 02=05, 03=12, 04=09, 06=11.
  So ~9 unique oracles.

**Interpretation**:
- K562 and HepG2 are identical across all 14 evals → same oracle.
- SKNSH oracle responds significantly to random content alone — perhaps
  its training distribution included many low-activity random-like sequences.
- We need K562/HepG2-activating sequences (motifs) to lift those scores.
