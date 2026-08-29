"""Palindrome + scaffold combo.

Each sequence is a full RC palindrome (complement 0<->3, 1<->2).
First 24 chars are a fixed period-4 scaffold "012301230123". The
scaffold "0123..." is self-RC-palindromic (so the last 24 chars also
become the scaffold automatically). Middle 152 chars are
random-then-revcomp (full palindrome structure).

Combines:
- Palindrome (b boost from internal RC symmetry, exp 012 = +0.11)
- Cross-sequence scaffold (b boost from positional alignment, exp 005)
Total fixed cross-sequence positions = 48 (24 prefix + 24 suffix),
well below the c cliff (~80).
"""
import numpy as np
import os

rng = np.random.default_rng(1414)
N, L = 50000, 200
SCAF_LEN = 24
scaffold = np.tile([0, 1, 2, 3], SCAF_LEN // 4).astype(np.uint8)
assert scaffold.size == SCAF_LEN

HALF = L // 2  # 100

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
unique, counts = np.unique(arr, return_counts=True)
print("composition:", {int(u): float(c) / arr.size for u, c in zip(unique, counts)})
# Sanity: confirm first 24 are scaffold and last 24 mirror correctly
print("first 24 of row 0:", arr[0, :24].tolist())
print("last 24 of row 0:", arr[0, -24:].tolist())
