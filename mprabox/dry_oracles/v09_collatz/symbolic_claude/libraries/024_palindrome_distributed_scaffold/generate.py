"""Palindrome + 4 distributed 6-char period-4 scaffolds in left half.

24 total scaffold positions in left half (matches 014's count) but
distributed at positions 0,25,50,75 of length-100 left half — gives b
4 anchor points spread across sequence instead of one prefix block.

H4: does b reward MORE anchor points (cross-sequence alignment sites)
than just contiguous scaffold? c should be fine since same # fixed.
"""
import numpy as np
import os

rng = np.random.default_rng(2424)
N, L = 50000, 200
HALF = L // 2  # 100

# 4 scaffold blocks of 6 chars each, period-4 "012301"
SCAF_BLOCK = np.array([0, 1, 2, 3, 0, 1], dtype=np.uint8)
BLOCK_LEN = len(SCAF_BLOCK)
POSITIONS = [0, 25, 50, 75]  # start positions of each block in left half

left = rng.integers(0, 4, size=(N, HALF), dtype=np.uint8)
for pos in POSITIONS:
    left[:, pos:pos + BLOCK_LEN] = SCAF_BLOCK

right = (3 - left).astype(np.uint8)[:, ::-1]
arr = np.concatenate([left, right], axis=1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
