#!/usr/bin/env python3
"""Experiment 009: per-row Markov chain.

Each row has a transition matrix T (4x4), with each row of T drawn from Dir(α=1).
- Some rows will have peaked transitions (cluster letters).
- Some will look near-uniform (like iid).
- Initial state uniform.
- Adds dinucleotide-level variance ACROSS rows beyond composition.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 23
ALPHA = np.array([1.0, 1.0, 1.0, 1.0])
K = 4  # alphabet size

rng = np.random.default_rng(SEED)
chars = np.array(['0', '1', '2', '3'])
out_arr = np.empty((N, L), dtype=np.uint8)

for i in range(N):
    # Draw transition matrix: each row Dir(α=1)
    T = rng.dirichlet(ALPHA, size=K)  # shape (K, K), T[k, j] = P(next=j | current=k)
    cum = np.cumsum(T, axis=1)  # for inverse-CDF sampling
    # Initial state uniform
    state = rng.integers(0, K)
    seq = np.empty(L, dtype=np.uint8)
    seq[0] = state
    u = rng.random(L - 1)
    for t in range(1, L):
        state = np.searchsorted(cum[state, :-1], u[t - 1])
        seq[t] = state
    out_arr[i] = seq

lines = chars[out_arr]
out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for row in lines:
        f.write(''.join(row.tolist()))
        f.write('\n')

print(f"Wrote {N} Markov-chain lines length {L} with per-row Dir(α=1) transitions")
