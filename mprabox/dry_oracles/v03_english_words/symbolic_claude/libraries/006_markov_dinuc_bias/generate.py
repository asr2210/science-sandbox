"""Experiment 006: Markov order-1 with dinucleotide bias.

Use a symmetric Markov chain on {0,1,2,3} where stationary distribution
is uniform but specific transitions are enriched:
  0 -> 1 with prob 0.55 (others 0.15 each)
  1 -> 0 with prob 0.55 (others 0.15 each)
  2 -> 3 with prob 0.55 (others 0.15 each)
  3 -> 2 with prob 0.55 (others 0.15 each)

By symmetry, stationary distribution is uniform 25% each. But dinucleotides
"01", "10", "23", "32" are enriched (~13.75% each vs 6.25% iid).

Tests whether dinucleotide structure helps (beyond pure composition).
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(101)

# Transition matrix
P = np.full((4, 4), 0.15)
P[0, 1] = 0.55; P[0, 0] = 0.15; P[0, 2] = 0.15; P[0, 3] = 0.15
P[1, 0] = 0.55; P[1, 1] = 0.15; P[1, 2] = 0.15; P[1, 3] = 0.15
P[2, 3] = 0.55; P[2, 0] = 0.15; P[2, 1] = 0.15; P[2, 2] = 0.15
P[3, 2] = 0.55; P[3, 0] = 0.15; P[3, 1] = 0.15; P[3, 3] = 0.15
# normalize rows
P = P / P.sum(axis=1, keepdims=True)

# Stationary: by symmetry should be uniform
# Verify quickly
w, v = np.linalg.eig(P.T)
idx = np.argmin(np.abs(w - 1))
stat = np.real(v[:, idx])
stat = stat / stat.sum()
print("Stationary distribution:", stat)

# Sample sequences
with open("sequences_0.txt", "w") as f:
    for _ in range(N):
        seq = np.empty(L, dtype=np.uint8)
        seq[0] = rng.choice(4, p=stat)
        for j in range(1, L):
            seq[j] = rng.choice(4, p=P[seq[j-1]])
        f.write("".join(chr(48 + c) for c in seq))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}")
