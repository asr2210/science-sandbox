"""Experiment 002: GC-rich biased random sequences (~60% GC).
50,000 sequences of 200bp.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPH = np.array(["A", "C", "G", "T"])
# Probabilities: 0.20 A, 0.30 C, 0.30 G, 0.20 T -> 60% GC
P = np.array([0.20, 0.30, 0.30, 0.20])

rng = np.random.default_rng(43)
idx = rng.choice(4, size=(N, L), p=P)
seqs = ["".join(ALPH[row]) for row in idx]

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N} sequences to {OUT}")
