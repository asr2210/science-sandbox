"""Exp 001: Uniform random 200bp sequences.
Pure baseline. 25% each of A/C/G/T. Seed fixed.
"""
import numpy as np
import os

N = 50_000
L = 200
rng = np.random.default_rng(0)
bases = np.array(list("ACGT"))
arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr]
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")
print(f"Wrote {N} sequences of length {L} to {out_path}")
