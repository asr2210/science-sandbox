"""Exp 009: per-sequence Markov chain with random transition matrix.

Adds dinucleotide composition variance on top of unigram variance.

For each sequence:
- Initial distribution from Dirichlet(2.0)
- 4x4 transition matrix; each row from Dirichlet(1.0)
- Walk the chain for 200 steps
"""
import os
import numpy as np

np.random.seed(20260608)

N = 50_000
L = 200
K = 4  # alphabet size

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N):
        init = np.random.dirichlet(np.full(K, 2.0))
        # Each row of the transition matrix from Dirichlet(1.0).
        T = np.random.dirichlet(np.full(K, 1.0), size=K)  # shape (K, K)
        # Walk.
        seq = np.empty(L, dtype=np.int8)
        seq[0] = np.random.choice(K, p=init)
        for t in range(1, L):
            seq[t] = np.random.choice(K, p=T[seq[t - 1]])
        f.write("".join(str(int(c)) for c in seq) + "\n")
print(f"wrote {N} per-sequence Markov sequences")
