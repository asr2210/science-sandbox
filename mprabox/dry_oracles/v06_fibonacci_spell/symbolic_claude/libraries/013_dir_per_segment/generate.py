#!/usr/bin/env python3
"""Experiment 013: per-row split-half compositions.

Each row: positions 0-99 sampled iid from p_left ~ Dir(α=1).
          positions 100-199 sampled iid from p_right ~ Dir(α=1).
- Adds internal positional/segment structure.
- Same overall iid-like local sampling within each segment.
"""
import os
import numpy as np

N = 50_000
L = 200
HALF = L // 2
SEED = 41
ALPHA = np.array([1.0, 1.0, 1.0, 1.0])

rng = np.random.default_rng(SEED)
chars = np.array(['0', '1', '2', '3'])

ps_left = rng.dirichlet(ALPHA, size=N)
ps_right = rng.dirichlet(ALPHA, size=N)
cum_left = np.cumsum(ps_left, axis=1)
cum_right = np.cumsum(ps_right, axis=1)
u_left = rng.random((N, HALF))
u_right = rng.random((N, HALF))

out_arr = np.empty((N, L), dtype=np.uint8)
for i in range(N):
    out_arr[i, :HALF] = np.searchsorted(cum_left[i, :-1], u_left[i])
    out_arr[i, HALF:] = np.searchsorted(cum_right[i, :-1], u_right[i])

lines = chars[out_arr]
out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for row in lines:
        f.write(''.join(row.tolist()))
        f.write('\n')

print(f"Wrote {N} lines length {L}, per-segment Dir(α=1) compositions")
