#!/usr/bin/env python3
"""Experiment 005: 50K strings, each with exactly 50 of each {0,1,2,3}, shuffled.

Kills per-string composition variance. Within-string order varies.
- If features depend only on composition → all features identical → NaN.
- If features depend on order/motifs → score depends on relationship.
"""
import os
import numpy as np

N = 50_000
L = 200
PER_LETTER = 50  # L / 4

rng = np.random.default_rng(123)

# Base array: 50 0s, 50 1s, 50 2s, 50 3s
base = np.repeat([0, 1, 2, 3], PER_LETTER).astype(np.uint8)
assert base.shape == (L,)

chars = np.array(['0', '1', '2', '3'])
out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')

with open(out_path, 'w') as f:
    for _ in range(N):
        perm = rng.permutation(L)
        shuffled = base[perm]
        f.write(''.join(chars[shuffled].tolist()))
        f.write('\n')

print(f"Wrote {N} lines length {L} (50 each letter, shuffled within string)")
