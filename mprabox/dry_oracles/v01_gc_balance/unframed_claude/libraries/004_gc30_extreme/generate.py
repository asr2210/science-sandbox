"""Experiment 004: Extreme AT bias (30% GC).
Tests whether the AT-rich -> better score trend continues monotonically.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPH = np.array(["A", "C", "G", "T"])
# P(A)=P(T)=0.35, P(C)=P(G)=0.15 -> 30% GC
P = np.array([0.35, 0.15, 0.15, 0.35])

rng = np.random.default_rng(45)
idx = rng.choice(4, size=(N, L), p=P)
seqs = ["".join(ALPH[row]) for row in idx]

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N} sequences to {OUT}")
