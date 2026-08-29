#!/usr/bin/env python3
"""Experiment 019: Dir(α=1) replicated with different seed.

Identical recipe to exp 006 (per-row p ~ Dir(1,1,1,1), 200 iid positions),
only the seed differs.
- exp 006 used SEED=11 → 0.1382
- this uses SEED=23
Purpose: characterize seed-to-seed variance of the best recipe family.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 23
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

print(f"Wrote {N} lines length {L}; Dir(α=1); SEED={SEED}")
