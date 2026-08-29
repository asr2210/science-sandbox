#!/usr/bin/env python3
"""Experiment 004: uniform random strings, SORTED by '0' count ascending.

Same string population as exp 001 (uniform random with seed 42).
Difference: rows are ordered by ascending count of '0'.

Goal: isolate row-order effect (composition unchanged from random library, only order).
"""
import os
import numpy as np

N = 50_000
L = 200
ALPHA = 4
SEED = 42  # same as exp 001

rng = np.random.default_rng(SEED)
arr = rng.integers(0, ALPHA, size=(N, L), dtype=np.uint8)

# count of '0' per row
zero_counts = (arr == 0).sum(axis=1)
order = np.argsort(zero_counts, kind='stable')  # ascending
arr_sorted = arr[order]

chars = np.array(['0', '1', '2', '3'])
lines = chars[arr_sorted]

out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for row in lines:
        f.write(''.join(row.tolist()))
        f.write('\n')

# Diagnostics
print(f"Wrote {N} lines length {L} sorted by '0'-count ascending")
print(f"Min '0'-count: {zero_counts.min()}, Max: {zero_counts.max()}, Median: {int(np.median(zero_counts))}")
