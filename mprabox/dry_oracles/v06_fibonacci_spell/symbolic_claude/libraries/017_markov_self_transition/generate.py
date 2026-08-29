#!/usr/bin/env python3
"""Experiment 017: per-row Markov self-transition probability.

Each row: r_i ~ Uniform[0.1, 0.9].
P(next = current) = r_i. P(next = each other) = (1 - r_i) / 3.
- Tests if intermediate clusteriness (between iid and blocks) helps.
- iid corresponds to r ≈ 0.25; blocks to r ≈ 1.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 89

rng = np.random.default_rng(SEED)
chars = np.array(['0', '1', '2', '3'])

rs = rng.uniform(0.1, 0.9, size=N)
# Initial states uniform
init = rng.integers(0, 4, size=N)
u = rng.random((N, L - 1))  # uniform draws for transitions

out_arr = np.empty((N, L), dtype=np.uint8)
out_arr[:, 0] = init.astype(np.uint8)
# Transition: with prob r stay, with prob (1-r) jump to one of other 3 uniformly
# Each "other" letter has probability (1-r)/3
# We'll do per-row vectorized: at each step, decide stay vs jump, and if jump, pick which.
for i in range(N):
    r = rs[i]
    other_p = (1.0 - r) / 3.0
    # Pre-draw two uniforms per transition for: (stay/jump), then which of 3 others
    u_stay = u[i]  # for stay/jump decision (already drawn)
    u_other = rng.random(L - 1)  # for which other letter
    state = init[i]
    for t in range(1, L):
        if u_stay[t - 1] < r:
            pass  # stay
        else:
            # pick one of the 3 other letters uniformly
            offset = int(u_other[t - 1] * 3) + 1  # 1, 2, or 3
            state = (state + offset) % 4
        out_arr[i, t] = state

lines = chars[out_arr]
out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for row in lines:
        f.write(''.join(row.tolist()))
        f.write('\n')

print(f"Wrote {N} lines; per-row r ~ U[0.1, 0.9]; mean r={rs.mean():.2f}")
