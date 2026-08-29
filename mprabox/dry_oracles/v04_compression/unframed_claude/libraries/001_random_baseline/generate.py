"""Experiment 001: Uniform random 200bp sequences.

Generates 50,000 sequences with uniform i.i.d. {A,C,G,T} at each position.
Baseline to anchor the score distribution.
"""
import numpy as np
import os

N_SEQ = 50000
LEN = 200
ALPHABET = np.array(list("ACGT"))

rng = np.random.default_rng(20260602)
idx = rng.integers(0, 4, size=(N_SEQ, LEN))
seqs = ["".join(ALPHABET[row]) for row in idx]

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N_SEQ} sequences of length {LEN} to {out_path}")
