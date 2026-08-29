"""Exp 004: each sequence has exactly 100 GC and 100 AT positions, shuffled.

Within GC positions, char is 1 or 2 uniformly. Within AT, char is 0 or 3 uniformly.
This eliminates per-sequence GC-fraction variance while keeping all 4 letters present.

Tests whether removing GC variance helps (r > 0.42), hurts (r < 0.42), or is
neutral compared to random uniform.
"""
import os
import numpy as np

N = 50_000
L = 200
HALF = L // 2  # 100
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

rng = np.random.default_rng(4)

# For each sequence, decide which positions are GC vs AT (shuffle a fixed pattern)
# Build a (N, L) bool array: True = GC.
template = np.array([True]*HALF + [False]*HALF)
# Shuffle each row independently
is_gc = np.tile(template, (N, 1))
# Vectorized shuffle each row
idx = np.argsort(rng.random((N, L)), axis=1)
is_gc = np.take_along_axis(is_gc, idx, axis=1)

sub = rng.integers(0, 2, size=(N, L), dtype=np.int8)
chars = np.where(is_gc, 1 + sub, 0 + 3 * sub).astype(np.int8)
chars += ord('0')

with open(OUT, "wb") as f:
    for i in range(N):
        f.write(bytes(chars[i].tolist()))
        f.write(b"\n")

# Sanity check
gc_counts = is_gc.sum(axis=1)
print(f"GC count per seq: min={gc_counts.min()} max={gc_counts.max()} (should all be {HALF})")
print(f"Wrote {N} fixed-GC50 sequences to {OUT}")
