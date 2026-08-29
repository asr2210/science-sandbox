"""Experiment 001: Random uniform DNA baseline.

50,000 sequences of 200bp, each base sampled i.i.d. uniform from {A,C,G,T}.
Establishes the noise floor for the black-box scorer.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 42

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N_SEQ, LEN))
mat = bases[idx]
seqs = ["".join(row) for row in mat]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N_SEQ} sequences x {LEN}bp to {out_path}")
