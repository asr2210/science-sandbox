"""Reverse-complement palindromic sequences.

Each sequence: 100 random chars + reverse-complement of those 100.
Complement: 0<->3, 1<->2 (DNA-like).

Tests if palindromic structure is rewarded (common in real TF
binding sites).
"""
import numpy as np
import os

rng = np.random.default_rng(1212)
N, L = 50000, 200
HALF = L // 2

left = rng.integers(0, 4, size=(N, HALF), dtype=np.uint8)
# Complement: 0->3, 1->2, 2->1, 3->0  => c[x] = 3 - x
comp = (3 - left).astype(np.uint8)
right = comp[:, ::-1]
arr = np.concatenate([left, right], axis=1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
unique, counts = np.unique(arr, return_counts=True)
print("composition:", {int(u): float(c) / arr.size for u, c in zip(unique, counts)})
