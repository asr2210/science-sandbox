"""Palindrome under alternative complement mapping 0<->1, 2<->3.

If b is specifically tuned to 0<->3, 1<->2 (DNA-like), this gives no
boost. If b detects any RC palindromic structure, this also boosts.
"""
import numpy as np
import os

rng = np.random.default_rng(1919)
N, L = 50000, 200
HALF = L // 2

left = rng.integers(0, 4, size=(N, HALF), dtype=np.uint8)

# Alternative complement: 0<->1, 2<->3.
# Map via lookup table.
COMP_ALT = np.array([1, 0, 3, 2], dtype=np.uint8)
comp = COMP_ALT[left]
right = comp[:, ::-1]
arr = np.concatenate([left, right], axis=1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
