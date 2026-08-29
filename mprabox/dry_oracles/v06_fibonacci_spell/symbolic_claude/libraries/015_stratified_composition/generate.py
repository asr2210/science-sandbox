#!/usr/bin/env python3
"""Experiment 015: stratified composition spread.

5 strata of 10K rows each:
- p_dom in [0.25, 0.3] (near-uniform)
- p_dom in [0.3, 0.45] (weak bias)
- p_dom in [0.45, 0.6] (moderate)
- p_dom in [0.6, 0.8] (strong)
- p_dom in [0.8, 0.95] (extreme)

Each row: random dominant letter; p[dom] ~ U[stratum]; p[others] = (1-p_dom)/3.
"""
import os
import numpy as np

N_PER = 10_000
L = 200
SEED = 67

rng = np.random.default_rng(SEED)
chars = np.array(['0', '1', '2', '3'])

strata = [(0.25, 0.30), (0.30, 0.45), (0.45, 0.60), (0.60, 0.80), (0.80, 0.95)]
N = N_PER * len(strata)
ps = np.empty((N, 4), dtype=np.float64)
idx = 0
for (lo, hi) in strata:
    for _ in range(N_PER):
        d = rng.integers(0, 4)
        p_dom = rng.uniform(lo, hi)
        p_other = (1.0 - p_dom) / 3.0
        ps[idx, :] = p_other
        ps[idx, d] = p_dom
        idx += 1

assert idx == N

# Shuffle rows so strata are interleaved (cosmetic; order doesn't matter for scoring)
order = rng.permutation(N)
ps = ps[order]

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

print(f"Wrote {N} lines length {L} (stratified compositions)")
