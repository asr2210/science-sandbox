"""Per-sequence random Markov chains.

Each of 50,000 sequences has its OWN random 4x4 transition matrix sampled from
Dirichlet(0.5) per row. Then a length-200 sequence is drawn from that Markov.

This diversifies dinucleotide stats across the 50k (going beyond mere composition
diversity from Dirichlet on monomers). Tests whether dinucleotide patterns are
a relevant axis.
"""
import numpy as np
import os

SEED = 89
N = 50000
L = 200
ALPHA = "0123"

rng = np.random.default_rng(SEED)

# Sample N transition matrices, each row from Dirichlet(0.5,0.5,0.5,0.5)
T = rng.dirichlet(np.full(4, 0.5), size=(N, 4))  # (N, 4, 4)

arr = np.empty((N, L), dtype=np.uint8)
# Start state: random uniform
arr[:, 0] = rng.integers(0, 4, size=N, dtype=np.uint8)

# For each step, draw from transition matrix
for j in range(1, L):
    prev = arr[:, j - 1]
    u = rng.random(size=N)
    # cum probs for each sequence's relevant row
    cum = np.cumsum(T[np.arange(N), prev], axis=1)  # (N, 4)
    arr[:, j] = (u[:, None] < cum).argmax(axis=1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

# Sanity
print(f"First seq composition: {np.bincount(arr[0], minlength=4) / L}")
print(f"Wrote {N} per-seq-Markov sequences to {out_path}")
