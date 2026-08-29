"""Experiment 004: Random uniform DNA, different seed (noise-floor control).

Replicates exp 001 with seed=99 instead of 42. Lets me quantify the
sequence-sampling noise in the score so I can tell real signal from noise
in subsequent experiments.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 99

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N_SEQ, LEN))
mat = bases[idx]
seqs = ["".join(row) for row in mat]
with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N_SEQ} seqs x {LEN}bp, seed={SEED}")
