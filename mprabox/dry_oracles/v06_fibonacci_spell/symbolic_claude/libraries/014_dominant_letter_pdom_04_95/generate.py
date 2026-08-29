#!/usr/bin/env python3
"""Experiment 014: forced-extremity per-row dominant letter.

For each row:
- Pick dominant letter d uniformly from {0,1,2,3}.
- Pick p_dom uniformly from [0.4, 0.95].
- p[d] = p_dom, p[others] = (1-p_dom)/3.
- Sample 200 positions iid from p.

Tests whether forcing all strings to be moderately-to-extremely biased
beats Dir(α=1) (which has ~25% strings near uniform).
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 53

rng = np.random.default_rng(SEED)
chars = np.array(['0', '1', '2', '3'])

dom_letters = rng.integers(0, 4, size=N)
p_doms = rng.uniform(0.4, 0.95, size=N)

ps = np.empty((N, 4), dtype=np.float64)
for i in range(N):
    p_other = (1.0 - p_doms[i]) / 3.0
    ps[i, :] = p_other
    ps[i, dom_letters[i]] = p_doms[i]

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

print(f"Wrote {N} lines length {L}; mean p_dom={p_doms.mean():.2f}")
