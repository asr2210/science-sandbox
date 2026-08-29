#!/usr/bin/env python3
"""Experiment 027: per-row α mix replicated with SEED=314."""
import os
import numpy as np

N = 50_000
L = 200
SEED = 314

rng = np.random.default_rng(SEED)
chars = np.array(['0', '1', '2', '3'])

alphas = rng.uniform(0.5, 2.0, size=N)
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

print(f"Wrote {N} lines; SEED={SEED}")
