"""Experiment 001: Random uniform sequence baseline.

50,000 sequences of 200bp drawn iid from uniform {A,C,G,T}.
Establishes a floor for model performance with no regulatory grammar.
"""
import numpy as np
import os

SEED = 42
N = 50_000
L = 200

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))

# Vectorized: produce N*L integer codes 0..3, index into alphabet
idx = rng.integers(0, 4, size=(N, L))
arr = alphabet[idx]
seqs = ["".join(row) for row in arr]

assert len(seqs) == N
assert all(len(s) == L for s in seqs)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"wrote {N} sequences of length {L} to {out_path}")
