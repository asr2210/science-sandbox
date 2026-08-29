#!/usr/bin/env python3
"""Experiment 007: Dirichlet(α=0.3) per-row composition.

More peaked Dirichlet (α < 1 favors corners). More composition variance.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 17
ALPHA_VAL = 0.3
ALPHA = np.array([ALPHA_VAL, ALPHA_VAL, ALPHA_VAL, ALPHA_VAL])

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

mean_p = ps.mean(axis=0)
std_p = ps.std(axis=0)
print(f"Wrote {N} lines length {L}, Dirichlet(α={ALPHA_VAL})")
print(f"  Per-row p means: {mean_p}")
print(f"  Per-row p stds:  {std_p}")
