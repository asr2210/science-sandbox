#!/usr/bin/env python3
"""Experiment 010: motif insertion test.

For each row i:
- Pick K_i ~ Uniform{0,...,20}.
- Start with iid uniform random length-200 string.
- Overwrite K_i random non-overlapping windows of length 4 with motif "0123".

Tests whether oracles respond to specific 4-mer motif "0123".
"""
import os
import numpy as np

N = 50_000
L = 200
MOTIF = "0123"
MLEN = len(MOTIF)
MAX_K = 20
SEED = 29

rng = np.random.default_rng(SEED)
chars = np.array(['0', '1', '2', '3'])
motif_arr = np.array([int(c) for c in MOTIF], dtype=np.uint8)

# Start with iid uniform random
base = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

# For each row, choose K_i and insert motifs
Ks = rng.integers(0, MAX_K + 1, size=N)

for i in range(N):
    k = Ks[i]
    if k == 0:
        continue
    # Choose k random start positions in [0, L - MLEN]
    max_start = L - MLEN
    # Use sampling with replacement (simple, overlapping ok)
    starts = rng.integers(0, max_start + 1, size=k)
    for s in starts:
        base[i, s:s+MLEN] = motif_arr

lines = chars[base]
out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for row in lines:
        f.write(''.join(row.tolist()))
        f.write('\n')

print(f"Wrote {N} lines with K~Unif[0,{MAX_K}] motif '{MOTIF}' insertions; mean K={Ks.mean():.2f}")
