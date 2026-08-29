"""Four palindromes per sequence (each length 50).

Each sequence = concatenation of 4 RC palindromes, each of length 50
(25 random + 25 revcomp). Total length 200; total RC pairs = 100.

Tests whether b prefers many short palindromes or one big palindrome.
Same total pair count as exp 012.
"""
import numpy as np
import os

rng = np.random.default_rng(1616)
N, L = 50000, 200
NUM_BLOCKS = 4
BLOCK = L // NUM_BLOCKS  # 50
HALF = BLOCK // 2        # 25

arr = np.empty((N, L), dtype=np.uint8)
for b in range(NUM_BLOCKS):
    left = rng.integers(0, 4, size=(N, HALF), dtype=np.uint8)
    right = (3 - left).astype(np.uint8)[:, ::-1]
    arr[:, b * BLOCK:b * BLOCK + HALF] = left
    arr[:, b * BLOCK + HALF:(b + 1) * BLOCK] = right

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
