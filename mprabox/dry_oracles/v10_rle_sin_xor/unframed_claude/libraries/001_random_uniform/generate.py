"""Experiment 001: 50,000 uniform random 200bp sequences. Baseline."""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPHABET = np.array(list("ACGT"))

rng = np.random.default_rng(0)
idx = rng.integers(0, 4, size=(N, L))
seqs = ["".join(ALPHABET[row]) for row in idx]

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"wrote {len(seqs)} sequences to {OUT}")
