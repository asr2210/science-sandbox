#!/usr/bin/env python3
"""Experiment 020: Dir(α=1) seed sweep, SEED=7."""
import os
import numpy as np

N = 50_000
L = 200
SEED = 7
ALPHA = np.array([1.0, 1.0, 1.0, 1.0])

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

print(f"Wrote {N} lines; SEED={SEED}")
