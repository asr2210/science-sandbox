"""Uniform random sequences with a 12-char balanced periodic motif
inserted at a random position in each sequence.

Motif = "012301230123" (perfectly balanced, period 4).
Sequence length 200; motif width 12 → motif covers 6% of bases.
"""
import numpy as np
import os

rng = np.random.default_rng(404)
N, L = 50000, 200
MOTIF = np.array([0, 1, 2, 3] * 3, dtype=np.uint8)  # length 12
MW = MOTIF.size

arr = rng.integers(0, 4, size=(N, L), dtype=np.uint8)
# Random insertion position for each row (uniform in [0, L-MW])
positions = rng.integers(0, L - MW + 1, size=N)
for i, p in enumerate(positions):
    arr[i, p:p + MW] = MOTIF

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
unique, counts = np.unique(arr, return_counts=True)
print("composition:", {int(u): float(c) / arr.size for u, c in zip(unique, counts)})
