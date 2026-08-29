"""Exp 001: random_uniform — baseline floor.

50,000 sequences x 200bp, each base i.i.d. uniform over ACGT.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
SEED = 42

rng = np.random.default_rng(SEED)
bases = np.array(["A", "C", "G", "T"])
idx = rng.integers(0, 4, size=(N, L), dtype=np.uint8)
seqs = bases[idx]
lines = ["".join(row) for row in seqs]

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"wrote {OUT}: {N} x {L}")
