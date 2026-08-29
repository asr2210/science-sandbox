"""Experiment 003: AT-rich biased random sequences (~40% GC).
Symmetric counterpart to 002.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPH = np.array(["A", "C", "G", "T"])
# P(A)=P(T)=0.30, P(C)=P(G)=0.20 -> 40% GC
P = np.array([0.30, 0.20, 0.20, 0.30])

rng = np.random.default_rng(44)
idx = rng.choice(4, size=(N, L), p=P)
seqs = ["".join(ALPH[row]) for row in idx]

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N} sequences to {OUT}")
