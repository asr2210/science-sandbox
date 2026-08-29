#!/usr/bin/env python3
"""Experiment 006: Dirichlet(1,1,1,1) per-row composition.

Each row: draw p ~ Dirichlet(α=1,1,1,1), then sample 200 positions iid from Categorical(p).
- α=1: uniform on the simplex (much wider per-row composition variance than exp 001 fixed-uniform).
- Symmetric across all 4 letters.
- Tests whether amplifying symmetric composition variance pushes b, c up.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 11
ALPHA = np.array([1.0, 1.0, 1.0, 1.0])

rng = np.random.default_rng(SEED)
chars = np.array(['0', '1', '2', '3'])

# Draw per-row p from Dirichlet(1,1,1,1)
ps = rng.dirichlet(ALPHA, size=N)  # shape (N, 4)

# For each row, sample L positions iid from Cat(p_row)
# Vectorize: build cumulative thresholds and use inverse CDF
cum = np.cumsum(ps, axis=1)  # (N, 4), last col ~1.0
u = rng.random((N, L))  # uniform
# For each (i, j), find smallest k such that u[i,j] < cum[i, k]
# Equivalent to searchsorted per-row.
out_arr = np.empty((N, L), dtype=np.uint8)
for i in range(N):
    out_arr[i] = np.searchsorted(cum[i, :-1], u[i])  # uses first 3 cumulative thresholds; values in {0,1,2,3}

lines = chars[out_arr]
out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for row in lines:
        f.write(''.join(row.tolist()))
        f.write('\n')

# Diagnostics
mean_p = ps.mean(axis=0)
std_p = ps.std(axis=0)
print(f"Wrote {N} lines length {L}, Dirichlet(α=1)")
print(f"  Per-row p means: {mean_p}")
print(f"  Per-row p stds:  {std_p}")
