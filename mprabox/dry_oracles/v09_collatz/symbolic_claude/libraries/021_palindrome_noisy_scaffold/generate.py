"""Palindrome + 48-char scaffold with 20% iid mutation noise on
scaffold positions.

Adds per-position cross-sequence variance to scaffold positions so
they aren't fully fixed — hopes to avoid the c cliff while keeping
the b alignment boost from a longer scaffold.

Each sequence: left half = scaffold(48, with 20% noise) +
random(52); right half = RC(left).
"""
import numpy as np
import os

rng = np.random.default_rng(2121)
N, L = 50000, 200
SCAF_LEN = 48
NOISE_P = 0.20
scaffold_base = np.tile([0, 1, 2, 3], SCAF_LEN // 4).astype(np.uint8)
HALF = L // 2

# Build left half
left = np.empty((N, HALF), dtype=np.uint8)
left[:, :SCAF_LEN] = scaffold_base  # broadcast
# Inject noise on scaffold positions
mut_mask = rng.random((N, SCAF_LEN)) < NOISE_P
random_chars = rng.integers(0, 4, size=(N, SCAF_LEN), dtype=np.uint8)
left[:, :SCAF_LEN] = np.where(mut_mask, random_chars, scaffold_base)
left[:, SCAF_LEN:] = rng.integers(0, 4, size=(N, HALF - SCAF_LEN), dtype=np.uint8)

right = (3 - left).astype(np.uint8)[:, ::-1]
arr = np.concatenate([left, right], axis=1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
unique, counts = np.unique(arr, return_counts=True)
print("composition:", {int(u): float(c) / arr.size for u, c in zip(unique, counts)})
