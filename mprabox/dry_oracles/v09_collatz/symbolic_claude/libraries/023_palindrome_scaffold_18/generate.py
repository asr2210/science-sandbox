"""Palindrome + 18-char period-4 scaffold prefix.

Exp 014 (24-scaffold) = 0.3066, Exp 017 (12-scaffold) = 0.3051,
Exp 015 (36-scaffold) = 0.3018. Try 18 to refine the sweet spot.
"""
import numpy as np
import os

rng = np.random.default_rng(2323)
N, L = 50000, 200
SCAF_LEN = 18  # 4.5 periods of "0123" -> use [0,1,2,3,0,1,2,3,...] truncated
HALF = L // 2

scaffold = np.array(([0, 1, 2, 3] * 5)[:SCAF_LEN], dtype=np.uint8)
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
