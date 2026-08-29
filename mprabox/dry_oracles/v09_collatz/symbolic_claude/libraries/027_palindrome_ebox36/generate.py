"""Palindrome + 36-char E-box scaffold (6x CACGTG).

Test whether longer E-box scaffold scales the boost. Exp 015 showed
generic 36 scaffold underperforms generic 24 (0.3018 vs 0.3066). But
since E-boxes are RC-palindromic AND a real motif, longer might help
b more without c collapse.
"""
import numpy as np
import os

rng = np.random.default_rng(2727)
N, L = 50000, 200
HALF = L // 2

EBOX = np.array([1, 0, 1, 2, 3, 2], dtype=np.uint8)  # CACGTG
scaffold = np.tile(EBOX, 6)  # length 36
SCAF_LEN = len(scaffold)
assert SCAF_LEN == 36

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
