"""Scaffold length 48 but content is a fixed RANDOM (non-periodic)
sequence, balanced composition. Tests whether periodicity vs alignment
explains 005's gain.
"""
import numpy as np
import os

rng_scaffold = np.random.default_rng(7000)
rng = np.random.default_rng(707)

N, L = 50000, 200
PREFIX_LEN = 48

# Random balanced scaffold: 12 of each char, shuffled
scaffold = np.array([0]*12 + [1]*12 + [2]*12 + [3]*12, dtype=np.uint8)
rng_scaffold.shuffle(scaffold)

arr = np.empty((N, L), dtype=np.uint8)
arr[:, :PREFIX_LEN] = scaffold
arr[:, PREFIX_LEN:] = rng.integers(0, 4, size=(N, L - PREFIX_LEN), dtype=np.uint8)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
print("scaffold:", "".join(str(x) for x in scaffold.tolist()))
unique, counts = np.unique(arr, return_counts=True)
print("composition:", {int(u): float(c) / arr.size for u, c in zip(unique, counts)})
