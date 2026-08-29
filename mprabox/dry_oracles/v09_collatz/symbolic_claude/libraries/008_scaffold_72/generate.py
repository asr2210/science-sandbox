"""Scaffold length 72 (period-4 prefix), bisecting 48 vs 100."""
import numpy as np
import os

rng = np.random.default_rng(808)
N, L = 50000, 200
PREFIX_LEN = 72
prefix = np.tile([0, 1, 2, 3], PREFIX_LEN // 4).astype(np.uint8)
assert prefix.size == PREFIX_LEN

arr = np.empty((N, L), dtype=np.uint8)
arr[:, :PREFIX_LEN] = prefix
arr[:, PREFIX_LEN:] = rng.integers(0, 4, size=(N, L - PREFIX_LEN), dtype=np.uint8)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
