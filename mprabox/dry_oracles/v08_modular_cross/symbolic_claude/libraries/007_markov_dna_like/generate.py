"""First-order Markov chain with approximate human-DNA dinucleotide frequencies.

Assumed mapping: 0=A, 1=C, 2=G, 3=T.
Captures CpG depletion and AT-bias typical of mammalian genomes.

Tests whether 'real-DNA-like' sequences (the kind models are trained on) score better.
"""
import numpy as np
import os

SEED = 23
N = 50000
L = 200
ALPHA = "0123"

# Transition matrix rows: from base 0/1/2/3, cols: to base 0/1/2/3
# Approximate human dinucleotide freq, normalized per row
T = np.array([
    [0.30, 0.20, 0.29, 0.21],   # from A
    [0.32, 0.27, 0.04, 0.37],   # from C (CpG depletion: C->G low)
    [0.30, 0.24, 0.27, 0.19],   # from G
    [0.18, 0.25, 0.30, 0.27],   # from T
])
# Compute stationary distribution from T (eigenvector for eigval 1)
eigvals, eigvecs = np.linalg.eig(T.T)
idx = np.argmin(np.abs(eigvals - 1.0))
stat = np.real(eigvecs[:, idx])
stat = stat / stat.sum()
print(f"Stationary distribution: {stat}")

rng = np.random.default_rng(SEED)

arr = np.empty((N, L), dtype=np.uint8)
# Start at stationary distribution
arr[:, 0] = rng.choice(4, size=N, p=stat)
# Markov chain
for j in range(1, L):
    prev = arr[:, j - 1]
    # For each row, draw from T[prev[i]]
    u = rng.random(size=N)
    cum = np.cumsum(T[prev], axis=1)  # (N, 4)
    arr[:, j] = (u[:, None] < cum).argmax(axis=1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

# Verify
char_counts = np.bincount(arr.ravel(), minlength=4)
print(f"Char counts: {char_counts / char_counts.sum()}")
print(f"Wrote {N} Markov-DNA-like sequences to {out_path}")
