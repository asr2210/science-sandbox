"""Experiment 001: pure random baseline.

50,000 uniform i.i.d. random 200bp ACGT sequences.
Purpose: establish floor performance for the eval sets.
"""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 42

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))

# generate as int array, then map to chars, then join — fast
idx = rng.integers(0, 4, size=(N_SEQ, LEN), dtype=np.int8)
seqs = alphabet[idx]
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join("".join(row) for row in seqs))
    f.write("\n")

print(f"Wrote {N_SEQ} sequences to {out_path}")
