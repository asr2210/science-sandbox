#!/usr/bin/env python3
"""Experiment 011: asymmetric Dirichlet biased toward '0'.

Dir((1.5, 0.5, 0.5, 0.5)) per-row p; sample iid 200 positions.
Mean p ≈ (0.5, 0.167, 0.167, 0.167).
Tests whether '0' has special status (vs symmetric Dir).
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 31
ALPHA = np.array([1.5, 0.5, 0.5, 0.5])

rng = np.random.default_rng(SEED)
chars = np.array(['0', '1', '2', '3'])
ps = rng.dirichlet(ALPHA, size=N)
cum = np.cumsum(ps, axis=1)
u = rng.random((N, L))

out_arr = np.empty((N, L), dtype=np.uint8)
for i in range(N):
    out_arr[i] = np.searchsorted(cum[i, :-1], u[i])

lines = chars[out_arr]
out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for row in lines:
        f.write(''.join(row.tolist()))
        f.write('\n')

print(f"Wrote {N} lines, Dir{tuple(ALPHA)}; mean p = {ps.mean(axis=0)}")
