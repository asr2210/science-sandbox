"""Experiment 001 — random uniform DNA baseline.

Generates 50,000 sequences of length 200 bp where each base is drawn
i.i.d. uniform from {A, C, G, T}. Establishes the floor for what a
model can learn when there is essentially no regulatory signal.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SEED = 1

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N, L))
seqs = alphabet[idx]

with open(OUT, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")

print(f"wrote {N} sequences of length {L} to {OUT}")
