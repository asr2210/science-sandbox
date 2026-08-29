#!/usr/bin/env python3
"""Experiment 003: row-monotonic '0' gradient.

For row i in 0..N-1:
  p_0(i) = i / (N - 1)    # probability of '0' at each position
  remaining mass 1 - p_0 split equally over {1, 2, 3}.

Each row is a length-200 random draw with that biased per-position distribution.
Row 0 has no '0's (random over {1,2,3}); row N-1 is all '0'.

Goal: test if row index matters and if '0'-content per row drives oracle output.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 7

rng = np.random.default_rng(SEED)
chars = np.array(['0', '1', '2', '3'])

# Pre-allocate
out_arr = np.empty((N, L), dtype=np.uint8)

p0s = np.linspace(0.0, 1.0, N)  # row-wise '0' probability
# For each row, sample with probabilities [p0, (1-p0)/3, (1-p0)/3, (1-p0)/3]
# Vectorize per row.
u = rng.random((N, L))
for i in range(N):
    p0 = p0s[i]
    rest = (1.0 - p0) / 3.0
    # cumulative thresholds [p0, p0+rest, p0+2*rest, 1.0]
    t1 = p0
    t2 = p0 + rest
    t3 = p0 + 2 * rest
    row_u = u[i]
    out = np.zeros(L, dtype=np.uint8)
    out[(row_u >= t1) & (row_u < t2)] = 1
    out[(row_u >= t2) & (row_u < t3)] = 2
    out[row_u >= t3] = 3
    out_arr[i] = out

lines = chars[out_arr]
out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for row in lines:
        f.write(''.join(row.tolist()))
        f.write('\n')

print(f"Wrote {N} lines length {L} with row-monotonic '0' gradient (seed={SEED})")
