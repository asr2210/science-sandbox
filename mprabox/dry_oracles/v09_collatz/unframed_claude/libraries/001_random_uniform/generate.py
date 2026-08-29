"""Experiment 001: uniform random sequences (25% each base).

Purpose: establish absolute baseline. Tells us where 'null' sequences
score so we can measure lift from designed libraries.
"""
import numpy as np

rng = np.random.default_rng(42)
N = 50_000
L = 200
BASES = np.array(list("ACGT"))

idx = rng.integers(0, 4, size=(N, L))
seqs = BASES[idx]

with open("libraries/001_random_uniform/sequences_0.txt", "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")

print(f"wrote {N} sequences of length {L}")
