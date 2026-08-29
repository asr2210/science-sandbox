"""Experiment 001: Random uniform baseline.
50,000 sequences of 200bp, uniform sampling from {A,C,G,T}.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPH = np.array(["A", "C", "G", "T"])

rng = np.random.default_rng(42)
idx = rng.integers(0, 4, size=(N, L))
seqs = ["".join(ALPH[row]) for row in idx]

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N} sequences to {OUT}")
