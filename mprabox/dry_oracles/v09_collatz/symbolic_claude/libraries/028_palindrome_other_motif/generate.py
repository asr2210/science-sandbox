"""Palindrome + 24-char alternative RC-palindromic motif (NOT E-box).

Test if E-box specifically helps or any 6-mer RC-palindromic motif.

Use "AATATT" = [0,0,3,0,3,3]: RC check —
complement [3,3,0,3,0,0] reversed [0,0,3,0,3,3]. RC-palindromic ✓.

If 028 matches 026 (~0.31), b rewards any RC-palindromic 6-mer
scaffold equally. If 028 < 026, E-box (GC-rich) is specifically
favored.
"""
import numpy as np
import os

rng = np.random.default_rng(2828)
N, L = 50000, 200
HALF = L // 2

MOTIF = np.array([0, 0, 3, 0, 3, 3], dtype=np.uint8)  # AATATT
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
