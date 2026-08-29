#!/usr/bin/env python3
"""Experiment 016: bimodal composition along (01|23) axis.

- 25K rows with p = (0.4, 0.4, 0.1, 0.1).
- 25K rows with p = (0.1, 0.1, 0.4, 0.4).
- iid sampled.

Tests whether features prefer composition variation along a specific bipartition.
"""
import os
import numpy as np

N_PER = 25_000
L = 200
SEED = 71

rng = np.random.default_rng(SEED)
chars = np.array(['0', '1', '2', '3'])

p_a = np.array([0.4, 0.4, 0.1, 0.1])
p_b = np.array([0.1, 0.1, 0.4, 0.4])

ps = np.tile(p_a, (N_PER, 1))
ps_b = np.tile(p_b, (N_PER, 1))
all_ps = np.vstack([ps, ps_b])
N = all_ps.shape[0]
# Shuffle for cosmetic interleaving (scoring is permutation-invariant)
all_ps = all_ps[rng.permutation(N)]

cum = np.cumsum(all_ps, axis=1)
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

print(f"Wrote {N} lines length {L} (bimodal 01 vs 23)")
