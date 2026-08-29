#!/usr/bin/env python3
"""Experiment 028: α mix with WIDER range U[0.3, 3.0], SEED=2026.

Exp 025 (α ~ U[0.5, 2.0], SEED=2026) was 0.1396 - best so far.
Test if widening α range helps the same seed.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 2026

rng = np.random.default_rng(SEED)
chars = np.array(['0', '1', '2', '3'])

alphas = rng.uniform(0.3, 3.0, size=N)
ps = np.empty((N, 4), dtype=np.float64)
for i in range(N):
    a = alphas[i]
    ps[i] = rng.dirichlet(np.array([a, a, a, a]))

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

print(f"Wrote {N} lines; α~U[0.3,3.0]; SEED={SEED}")
