"""Palindrome + 24-char RC-palindromic motif scaffold (E-box CACGTG x4).

If alphabet maps 0=A,1=C,2=G,3=T, then E-box "CACGTG" = [1,0,1,2,3,2].
This is RC-palindromic under 0<->3, 1<->2. Tile 4 copies = 24 chars.

Hypothesis: if scorer is regulation-like, an actual TF motif at fixed
position may add boost beyond generic period-4 scaffold. If not, score
should match 014 within noise (since fixed scaffold pattern alone).
"""
import numpy as np
import os

rng = np.random.default_rng(2626)
N, L = 50000, 200
HALF = L // 2

EBOX = np.array([1, 0, 1, 2, 3, 2], dtype=np.uint8)  # CACGTG
scaffold = np.tile(EBOX, 4)  # length 24, RC-palindromic
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
