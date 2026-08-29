"""Palindrome + 4x AAATTT scaffold (24 chars, AT-extreme palindrome).

028 with AATATT (more mixed AT) gave b=0.172. Try the AT-MAXIMAL
palindromic 6-mer "AAATTT" = [0,0,0,3,3,3]. RC-palindromic ✓.

If b reward scales with AT-purity, this should boost further. If b
rewards mixed AT patterns more, this could underperform 028.
"""
import numpy as np
import os

rng = np.random.default_rng(2929)
N, L = 50000, 200
HALF = L // 2

MOTIF = np.array([0, 0, 0, 3, 3, 3], dtype=np.uint8)  # AAATTT
scaffold = np.tile(MOTIF, 4)  # length 24
SCAF_LEN = len(scaffold)
assert SCAF_LEN == 24

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
