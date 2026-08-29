"""Direct repeat: each sequence = 100 random + same 100 (no complement).

Tests whether b rewards reverse-complement specifically (palindrome)
or any internal repeat / self-similarity.
"""
import numpy as np
import os

rng = np.random.default_rng(1313)
N, L = 50000, 200
HALF = L // 2

left = rng.integers(0, 4, size=(N, HALF), dtype=np.uint8)
arr = np.concatenate([left, left], axis=1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
