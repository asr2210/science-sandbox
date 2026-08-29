#!/usr/bin/env python3
"""Experiment 001: uniform random baseline.

50,000 strings of length 200, each char uniformly from {0,1,2,3}.
"""
import os
import numpy as np

N = 50_000
L = 200
ALPHA = 4
SEED = 42

rng = np.random.default_rng(SEED)
arr = rng.integers(0, ALPHA, size=(N, L), dtype=np.uint8)

# Convert to text efficiently
chars = np.array(['0', '1', '2', '3'])
lines = chars[arr]

out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for row in lines:
        f.write(''.join(row.tolist()))
        f.write('\n')

print(f"Wrote {N} lines of length {L} to {out_path}")
