"""Palindrome + 12-char scaffold prefix (24 fixed total)."""
import numpy as np
import os

rng = np.random.default_rng(1717)
N, L = 50000, 200
SCAF_LEN = 12
scaffold = np.tile([0, 1, 2, 3], SCAF_LEN // 4).astype(np.uint8)

HALF = L // 2
left = np.empty((N, HALF), dtype=np.uint8)
left[:, :SCAF_LEN] = scaffold
left[:, SCAF_LEN:] = rng.integers(0, 4, size=(N, HALF - SCAF_LEN), dtype=np.uint8)
right = (3 - left).astype(np.uint8)[:, ::-1]
arr = np.concatenate([left, right], axis=1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
