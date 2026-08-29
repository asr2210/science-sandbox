"""Experiment 008: AP-1 motif at RANDOM position (vs fixed in exp 002).

Tests whether the exp 002 drop was driven by FIXED POSITION (variance loss
at single columns) or by motif identity. If exp 008 ≈ exp 006 (0.328),
position drives the effect. If exp 008 ≈ exp 002 (0.278), motif identity
drives it.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
MOTIF = "TGAGTCA"
SEED = 48

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
mat = bases[rng.integers(0, 4, size=(N_SEQ, LEN))]

motif_arr = np.array(list(MOTIF))
positions = rng.integers(0, LEN - len(MOTIF) + 1, size=N_SEQ)
for i in range(N_SEQ):
    p = positions[i]
    mat[i, p:p + len(MOTIF)] = motif_arr

seqs = ["".join(row) for row in mat]
with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N_SEQ} seqs; AP-1 ({MOTIF}) at random position per seq")
