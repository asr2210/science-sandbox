"""Uniform random tail with a fixed balanced scaffold prefix.

First 50 chars = "01230123..." (period 4, balanced) — identical across
all 50k sequences. Last 150 chars = iid uniform random.

Tests whether condition b rewards cross-sequence alignment at fixed
positions (shared structure at the same coordinates).
"""
import numpy as np
import os

rng = np.random.default_rng(505)
N, L = 50000, 200
PREFIX_LEN = 48  # divisible by 4 to keep prefix exactly balanced
prefix = np.tile([0, 1, 2, 3], PREFIX_LEN // 4).astype(np.uint8)
assert prefix.size == PREFIX_LEN

arr = np.empty((N, L), dtype=np.uint8)
arr[:, :PREFIX_LEN] = prefix  # broadcast
arr[:, PREFIX_LEN:] = rng.integers(0, 4, size=(N, L - PREFIX_LEN), dtype=np.uint8)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
unique, counts = np.unique(arr, return_counts=True)
print("composition:", {int(u): float(c) / arr.size for u, c in zip(unique, counts)})
